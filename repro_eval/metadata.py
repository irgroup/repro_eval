import os
import json
import platform
import pkg_resources
import warnings
from collections import defaultdict
from io import BytesIO, TextIOWrapper
import cpuinfo
import pytrec_eval
import git
from ruamel.yaml import YAML
from repro_eval import Evaluator


class PrimadExperiment:
    def __init__(self, **kwargs): 
    
        self.ref_base_path = kwargs.get('ref_base_path', None)
        if self.ref_base_path:
            self.ref_base_run = MetadataHandler.strip_metadata(self.ref_base_path)
        else:
            self.ref_base_run = None
        
        self.ref_adv_path = kwargs.get('ref_adv_path', None)
        if self.ref_adv_path:
            self.ref_adv_run = MetadataHandler.strip_metadata(self.ref_adv_path)
        else:
            self.ref_adv_run = None    
        
        self.primad = kwargs.get('primad', None)
        
        self.rep_base = kwargs.get('rep_base', None)
        self.rpd_qrels = kwargs.get('rpd_qrels', None)
        self.rep_adv = kwargs.get('rep_adv', None)
        self.rpl_qrels = kwargs.get('rpl_qrels', None)

        if self.rpl_qrels:
            self.rep_eval = Evaluator.RplEvaluator(qrel_orig_path=self.rpd_qrels,
                                                   qrel_rpl_path=self.rpl_qrels)  
            
            with open(self.rpd_qrels, 'r') as f_rpd_qrels, open(self.rpl_qrels, 'r') as f_rpl_qrels:
                qrels = pytrec_eval.parse_qrel(f_rpd_qrels)
                self.rpd_rel_eval = pytrec_eval.RelevanceEvaluator(qrels, pytrec_eval.supported_measures)
                qrels = pytrec_eval.parse_qrel(f_rpl_qrels)
                self.rpl_rel_eval = pytrec_eval.RelevanceEvaluator(qrels, pytrec_eval.supported_measures)
            
        
        elif self.primad[-1].islower(): # check if data component is the same
            self.rep_eval = Evaluator.RpdEvaluator(qrel_orig_path=self.rpd_qrels)
            
            with open(self.rpd_qrels, 'r') as f_qrels:
                qrels = pytrec_eval.parse_qrel(f_qrels)
                self.rpd_rel_eval = pytrec_eval.RelevanceEvaluator(qrels, pytrec_eval.supported_measures)
            
        else:
            raise ValueError
            
    def get_primad_type(self):
        return self.primad
    
    def evaluate(self):
        
        if self.primad == 'priMad':
            if self.ref_adv_run is None and self.rep_adv is None:
                
                evaluations = {} 
                
                self.rep_eval.run_b_orig = self.ref_base_run
                self.rep_eval.evaluate()

                for rep_run_path in self.rep_base + [self.ref_base_path]:
                    
                    run_evaluations = {}
                
                    rep_run = MetadataHandler.strip_metadata(rep_run_path)
                    scores = self.rpd_rel_eval.evaluate(rep_run)
                    
                    run_evaluations['arp'] = scores
                    run_evaluations['ktu'] = self.rep_eval.ktau_union(run_b_rep=rep_run).get('baseline')
                    run_evaluations['rbo'] = self.rep_eval.rbo(run_b_rep=rep_run).get('baseline')
                    run_evaluations['rmse'] = self.rep_eval.nrmse(run_b_score=scores).get('baseline')
                    run_evaluations['pval'] = self.rep_eval.ttest(run_b_score=scores).get('baseline')
                
                    run_name = os.path.basename(rep_run_path)
                
                    evaluations[run_name] = run_evaluations
        
                return evaluations
    
        if self.primad == 'PRIMAd':
            
            evaluations = {} 
            
            self.rep_eval.run_b_orig = self.ref_base_run
            self.rep_eval.run_a_orig = self.ref_adv_run
            self.rep_eval.trim(t=1000)
            self.rep_eval.evaluate()
    
            pairs = self._find_pairs(rep_base=self.rep_base, rep_adv=self.rep_adv)
            pairs = pairs + [{'base': self.ref_base_path, 'adv': self.ref_adv_path}]
            
            for pair in pairs:
                
                pair_evaluations = {}
                
                rep_run_base = MetadataHandler.strip_metadata(pair.get('base'))
                rep_meta_base = MetadataHandler.read_metadata(pair.get('base'))                
                rep_run_adv = MetadataHandler.strip_metadata(pair.get('adv'))
                rep_meta_adv = MetadataHandler.read_metadata(pair.get('adv'))          
                      
                self.rep_eval.trim(t=1000, run=rep_run_base)
                self.rep_eval.trim(t=1000, run=rep_run_adv)
                scores_base = self.rpd_rel_eval.evaluate(rep_run_base)
                scores_adv = self.rpd_rel_eval.evaluate(rep_run_adv)
                arp = {'baseline': scores_base, 'advanced': scores_adv}
                pair_evaluations['arp'] = arp 
                pair_evaluations['ktu'] = self.rep_eval.ktau_union(run_b_rep=rep_run_base, run_a_rep=rep_run_adv)
                pair_evaluations['rbo'] = self.rep_eval.rbo(run_b_rep=rep_run_base, run_a_rep=rep_run_adv)
                pair_evaluations['rmse'] = self.rep_eval.nrmse(run_b_score=scores_base, run_a_score=scores_adv)
                pair_evaluations['er'] = self.rep_eval.er(run_b_score=scores_base, run_a_score=scores_adv)
                pair_evaluations['dri'] = self.rep_eval.dri(run_b_score=scores_base, run_a_score=scores_adv)
                pair_evaluations['pval'] = self.rep_eval.ttest(run_b_score=scores_base, run_a_score=scores_adv)
                
                if rep_meta_base.get('actor').get('team') == rep_meta_adv.get('actor').get('team'):
                    expid = rep_meta_base.get('actor').get('team')
                else:
                    expid = '_'.join([rep_meta_base.get('tag'), rep_meta_adv.get('tag')])
                
                evaluations[expid] = pair_evaluations
 
            return evaluations
    
        if self.primad == 'PRIMAD':
            evaluations = {} 
            
            self.rep_eval.run_b_orig = self.ref_base_run
            self.rep_eval.run_a_orig = self.ref_adv_run
            self.rep_eval.trim(t=1000)
            self.rep_eval.evaluate()
    
            pairs = self._find_pairs(rep_base=self.rep_base, rep_adv=self.rep_adv)
            pairs = pairs
            
            for pair in pairs:
                
                pair_evaluations = {}
                
                rep_run_base = MetadataHandler.strip_metadata(pair.get('base'))
                rep_meta_base = MetadataHandler.read_metadata(pair.get('base'))                
                rep_run_adv = MetadataHandler.strip_metadata(pair.get('adv'))
                rep_meta_adv = MetadataHandler.read_metadata(pair.get('adv'))          
                      
                self.rep_eval.trim(t=1000, run=rep_run_base)
                self.rep_eval.trim(t=1000, run=rep_run_adv)
                scores_base = self.rpl_rel_eval.evaluate(rep_run_base)
                scores_adv = self.rpl_rel_eval.evaluate(rep_run_adv)
                arp = {'baseline': scores_base, 'advanced': scores_adv}
                pair_evaluations['arp'] = arp 
                pair_evaluations['er'] = self.rep_eval.er(run_b_score=scores_base, run_a_score=scores_adv)
                pair_evaluations['dri'] = self.rep_eval.dri(run_b_score=scores_base, run_a_score=scores_adv)
                pair_evaluations['pval'] = self.rep_eval.ttest(run_b_score=scores_base, run_a_score=scores_adv)
                
                expid = '_'.join([rep_meta_base.get('tag'), rep_meta_adv.get('tag')])  
                evaluations[expid] = pair_evaluations
            
            return evaluations
        
    def _find_pairs(self, rep_base, rep_adv):

        pairs = []
        for brp in rep_base:
            br = MetadataHandler.read_metadata(run_path=brp)

            arp = None
            cnt = 0
            
            for _arp in rep_adv:
                _cnt = 0
                ar = MetadataHandler.read_metadata(run_path=_arp)
                
                for k,v in br.items():
                    if v == ar.get(k):
                        _cnt += 1
                        
                if _cnt > cnt:
                    cnt = _cnt 
                    arp = _arp
            
            pairs.append({'base': brp, 'adv': arp})
            
        return pairs
    

class MetadataAnalyzer:
    
    def __init__(self, run_path):
        
        self.reference_run_path = run_path
        self.reference_run = MetadataHandler.strip_metadata(run_path)
        self.reference_metadata = MetadataHandler.read_metadata(run_path)
        
    def set_reference(self, run_path):
        
        self.reference_run_path = run_path
        self.reference_run = MetadataHandler.strip_metadata(run_path)
        self.reference_metadata = MetadataHandler.read_metadata(run_path)
        
    def analyze_directory(self, dir_path):    
        
        components = ['platform', 'research goal', 'implementation', 'method', 'actor', 'data']
        primad = {}
        
        files = os.listdir(dir_path)
        
        for _file in files:
            file_path = os.path.join(dir_path, _file)
    
            if file_path == self.reference_run_path:
                continue
            
            _metadata = MetadataHandler.read_metadata(file_path)
            
            primad_str = ''
                                        
            for component in components:
                if self.reference_metadata[component] != _metadata[component]:
                    primad_str += component[0].upper()
                else:
                    primad_str += component[0]
            
            primad[file_path] = primad_str
            
        experiments = defaultdict(list)
        for k, v in primad.items(): 
            experiments[v].append(k)
            
        return experiments  
    
    @staticmethod
    def filter_by_baseline(ref_run, runs):
        
        run_tag = MetadataHandler.read_metadata(ref_run).get('tag')

        filtered_list = []
        for run in runs:
            _metadata = MetadataHandler.read_metadata(run)
            baseline = _metadata.get('research goal').get('evaluation').get('baseline')[0]
            if baseline == run_tag:
                filtered_list.append(run)
                
        return filtered_list
    
    @staticmethod 
    def filter_by_test_collection(test_collection, runs):
        
        filtered_list = []
        for run in runs:
            _metadata = MetadataHandler.read_metadata(run)
            name = _metadata.get('data').get('test_collection').get('name')
            if test_collection == name:
                filtered_list.append(run)
                
        return filtered_list


class MetadataHandler:
    def __init__(self, run_path, metadata_path=None):
         
        self.run_path = run_path
        
        if metadata_path:
            self._metadata = MetadataHandler.read_metadata_template(metadata_path)
        else:
            self._metadata = MetadataHandler.read_metadata(run_path)
        
    def get_metadata(self):
        
        return self._metadata
    
    def set_metadata(self, metadata_dict=None, metadata_path=None):
        
        if metadata_path:
            self._metadata = MetadataHandler.read_metadata_template(metadata_path)
        
        if metadata_dict:
            self._metadata = metadata_dict
    
    def dump_metadata(self, dump_path=None, complete_metadata=False, repo_path='.'):
                
        if complete_metadata:
            self.complete_metadata(repo_path=repo_path)
            
        if self._metadata:
                
            tag = self._metadata['tag'] 
            f_out_name = '_'.join([tag, 'dump.yml'])  
            f_out_path = os.path.join(dump_path, f_out_name)    
                
            with open(f_out_path, 'wb') as f_out:
                bytes_io = BytesIO()
                yaml = YAML()
                yaml.dump(self._metadata, bytes_io)
                f_out.write(bytes_io.getvalue())

    def write_metadata(self, run_path=None, complete_metadata=False, repo_path='.'):
        
        if complete_metadata:
            self.complete_metadata(repo_path=repo_path)
        
        bytes_io = BytesIO()
        yaml = YAML()
        yaml.dump(self._metadata, bytes_io)
    
        byte_str = bytes_io.getvalue().decode('UTF-8')
        lines = byte_str.split('\n')
        
        if run_path is None:
            f_out_path = '_'.join([self.run_path, 'annotated'])
        else:
            f_out_path = '_'.join([run_path])
        
        with open(f_out_path, 'w') as f_out:
            
            f_out.write('# METADATA - START\n')
            for line in lines[:-1]:
                f_out.write(' '.join(['#', line, '\n']))            
            f_out.write('# METADATA - END\n')
            
            with open(self.run_path, 'r') as f_in:
                for run_line in f_in.readlines():
                    f_out.write(run_line)
                
    def complete_metadata(self, repo_path='.'):
        if self._metadata.get('platform') is None:
            platform_dict = {
                'hardware': {
                    'cpu': self._get_cpu(),  
                    'ram': self._get_ram(),
                    },
                'operating system': self._get_os(),
                'software': self._get_libs(),
                }
            
            self._metadata['platform'] = platform_dict
            
        if self.metadata.get('implementation') is None: 
            self._metadata['implementation'] = self._get_src(repo_path=repo_path)
    
    @staticmethod
    def strip_metadata(annotated_run):
        '''
        Strips off the metadata and returns a dict-version of the run that is parsed with pytrec_eval.
        '''

        with TextIOWrapper(buffer=BytesIO(), encoding='utf-8', line_buffering=True) as text_io_wrapper:
            with open(annotated_run, 'r') as f_in:
                lines = f_in.readlines()
                for line in lines:
                    if line[0] != '#':
                        text_io_wrapper.write(line)
            text_io_wrapper.seek(0,0)        
            run = pytrec_eval.parse_run(text_io_wrapper)
                        
        return run

    @staticmethod
    def read_metadata(run_path):
        '''
        Reads the metadata out of an annotated run and returns a dict containing the metadata.
        '''
        
        _metadata = None
        
        with open(run_path, 'r') as f_in: 
            lines = f_in.readlines()
            if lines[0].strip('\n') == '# METADATA - START':
                metadata_str = ''
                yaml=YAML(typ='safe')

                for line in lines[1:]:
                    if line.strip('\n') != '# METADATA - END':
                        metadata_str += line.strip('#')
                    else:
                        break
                _metadata = yaml.load(metadata_str)
        
        return _metadata
    
    @staticmethod
    def read_metadata_template(template_path):
        with open(template_path, 'r') as f_in:
            yaml = YAML(typ='safe')
            return yaml.load(f_in)

    def _get_cpu(self):
        cpu = cpuinfo.get_cpu_info()
        return {
            'model': cpu['brand_raw'],
            'architecture': platform.machine(),
            'operation mode': '-'.join([str(cpu['bits']), 'bit']),
            'number of cores': cpu['count'],
        }
      
    def _get_os(self):
        try:
            with open("/etc/os-release") as f_in:
                os_info = {}
                for line in f_in:
                    k,v = line.rstrip().split("=")
                    os_info[k] = v.strip('"')
                
            distribution = os_info['PRETTY_NAME']
            
        except:
            warnings.warn('/etc/os-release not found. Using the available information of the platform package instead.')
            distribution = platform.version()
             
        return {
            'platform': platform.system(),
            'kernel': platform.release(),
            'distribution': distribution,
        }

    def _get_ram(self):
        memory_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') 
        memory_gb = memory_bytes/(1024.0 ** 3)  
        return {'ram': ' '.join([str(round(memory_gb, 2)),'GB'])}

    def _get_libs(self):
        installed_packages = [d.project_name for d in pkg_resources.working_set]
        return {'libraries': installed_packages}

    def _get_src(self, repo_path='.'):
        extensions_path = './resources/extensions.json'
        repo = git.Repo(repo_path)
        
        with open(extensions_path, 'r') as input_file:
            extensions = json.load(input_file)
        languages = set()

        for _, _, files in os.walk('.'):
            for name in files:
                _, file_extension = os.path.splitext(name)
                language = extensions.get(file_extension[1:])
                if language:
                    languages.add(language)

        return {
            'repository': repo.remote().url,
            'commit': str(repo.head.commit),
            'lang': list(languages),
        }