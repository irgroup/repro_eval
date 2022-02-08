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

META_START = '# ir_metadata.start'
META_END = '# ir_metadata.end'

class PrimadExperiment:
    """
    The PrimadExperiment is used to determine the reproducibility measures 
    between a reference run and a set of one or more reproduced run files.
    Depending on the type of the PRIMAD experiment, several reproducibility 
    measures can be determined.
    
    @param ref_base_path: Path to a single run file that corresponds to the 
                          original (or reference) baseline of the experiments. 
    @param ref_adv_path: Path to a single run file that corresponds to the
                         original (or reference) baseline of the experiments.
    @param primad: String with lower and upper case letters depending on which 
                   PRIMAD components have changed in the experiments, e.g., 
                   "priMad" when only the Method changes due to parameter sweeps.
    @param rep_base: List containing paths to run files that reproduce the 
                     original (or reference) baseline run.
    @param rpd_qrels: Qrels file that is used to evaluate the reproducibility of
                      the experiments, i.e., it used to evaluate runs that are 
                      derived from the same test collection.
    @param rep_adv: List containing paths to run files that reproduce the 
                    original (or reference) advanced run.
    @param rpl_qrels: Qrels file that is used to evaluate the replicability of
                      the experiments, i.e., it is used to evaluate runs that are 
                      derived from a different test collection. Please note that 
                      "rpd_qrels" has to be provided too.
    """
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
            raise ValueError('Please provide a correct combination of qrels and PRIMAD type.')
            
    def get_primad_type(self):
        """
        This method returns a string that identifies the type of the 
        PRIMAD experiment.

        @return: String with lower and upper case letters depending on which 
                 PRIMAD components have changed in the experiments, e.g., 
                 "priMad" when only the Method changes due to parameter sweeps.
        """
        return self.primad
    
    def evaluate(self):
        """
        This method validates the PRIMAD experiment in accordance with the given
        "primad" identifier. Currently, the following experiments are supported.
            - priMad: Parameter sweep
            - PRIMAd: Reproducibility evaluation on the same test collection
            - PRIMAD: Generalizability evaluation
        
        @return: Dictionary containing the average retrieval performance and 
                 the reproducibility measures for each run.
        """
        
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
        
        else:
            raise ValueError('The specified type of the PRIMAD experiments is not supported yet.')
        
    def _find_pairs(self, rep_base, rep_adv):
        """
        This method finds pairs between lists of baseline and advanced runs. 
        A pair is defined by the highest number of matching PRIMAD components.
        
        @param rep_base: List with baseline runs.
        @param rep_adv: List with advanced runs.
        
        @return: List with dictionaries containing paths to a baseline and an 
                 advanced run.
        """

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
    """
    The MetadataAnalyzer is used to analyze set of different run files in
    reference to a run that has be be provided upon instantiation. The 
    analyze_directory() method returns a dictionary with PRIMAD identifiers as
    keys and lists with the corresponding run paths as values.
    
    @param run_path: Path to the reference run file.
    """
    
    def __init__(self, run_path):
        
        self.reference_run_path = run_path
        self.reference_run = MetadataHandler.strip_metadata(run_path)
        self.reference_metadata = MetadataHandler.read_metadata(run_path)
        
    def set_reference(self, run_path):
        """
        Use this method to set a new reference run.
        
        @param run_path: Path to the new reference run file.
        """
        
        self.reference_run_path = run_path
        self.reference_run = MetadataHandler.strip_metadata(run_path)
        self.reference_metadata = MetadataHandler.read_metadata(run_path)
        
    def analyze_directory(self, dir_path):    
        """
        Use this method to analyze the specified directory in comparison to the 
        reference run. 
        
        @param dir_path: Path to the directory.
        """
        
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
        """
        Use this method to filter a list of runs wrt. to the baseline that is 
        specified under "research goal/evaluation/baseline" of a given reference run.
        
        @param ref_run: The reference with the baseline.
        @param runs: A list of run paths that is filtered.
        """
        
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
        """
        Use this method to filter a list of runs wrt. to the test collection
        specified under "data/test_collection".
        
        @param test_collection: Name of the test collection.
        @param runs: A list of run paths that is filtered.
        """
        
        filtered_list = []
        for run in runs:
            _metadata = MetadataHandler.read_metadata(run)
            name = _metadata.get('data').get('test collection').get('name')
            if test_collection == name:
                filtered_list.append(run)
                
        return filtered_list


class MetadataHandler:
    """
    Use the MetadataHandler for in- and output operations of annotated run files.
    
    @param run_path: Path the run file without metadata annotations. It is also 
                     possible to load an already annotated run and modify it with
                     the MetadataHandler.
    @param metadata_path: Path to the YAML file containing the metadata that 
                          should be added to the run file.
    """
    def __init__(self, run_path, metadata_path=None):
         
        self.run_path = run_path
        
        if metadata_path:
            self._metadata = MetadataHandler.read_metadata_template(metadata_path)
        else:
            self._metadata = MetadataHandler.read_metadata(run_path)
        
    def get_metadata(self):
        """
        Use this method to get the currently set metadata annotations.
        
        @return: Nested dictionary containing the metadata annotations.
        """
        
        return self._metadata
    
    def set_metadata(self, metadata_dict=None, metadata_path=None):
        """
        Use this method to set/update the metadata. It can either be provided with a 
        dictionary of a path to a YAML file
        
        @param metadata_dict: Nested dictionary containing the metadata annotations.
        @param metadata_path: Path to the YAML file with metadata.
        """
        if metadata_path:
            self._metadata = MetadataHandler.read_metadata_template(metadata_path)
        
        if metadata_dict:
            self._metadata = metadata_dict
    
    def dump_metadata(self, dump_path=None, complete_metadata=False, repo_path='.'):
        """
        Use this method to dump the current metadata into a YAML file. 
        The filename is a concatenation of the run tag and the "_annotated" suffix.
        
        @param dump_path: Path to the directory where the metadata is dumped.
        @param complete_metadata: If true, the Platform and Implementation will 
                                  be added automatically, if not already provided.
        @param repo_path: Path to the git repository of the Implementation that 
                          underlies the run file. This path is needed for the 
                          automatic completion.
        """
           
        if complete_metadata:
            self.complete_metadata(repo_path=repo_path)
            
        if self._metadata:
                
            tag = self._metadata['tag'] 
            f_out_name = '_'.join([tag, 'dump.yaml'])  
            f_out_path = os.path.join(dump_path, f_out_name)    
                
            with open(f_out_path, 'wb') as f_out:
                bytes_io = BytesIO()
                yaml = YAML()
                yaml.width = 4096
                yaml.dump(self._metadata, bytes_io)
                f_out.write(bytes_io.getvalue())

    def write_metadata(self, run_path=None, complete_metadata=False, repo_path='.'):
        """
        This method writes the metadata into the run file.
        
        @param run_path: Path to the annotated run file.
        @param complete_metadata: If true, the Platform and Implementation will 
                                  be added automatically, if not already provided.
        @param repo_path: Path to the git repository of the Implementation that 
                          underlies the run file. This path is needed for the 
                          automatic completion.
        """
        if complete_metadata:
            self.complete_metadata(repo_path=repo_path)
        
        bytes_io = BytesIO()
        yaml = YAML()
        yaml.width = 4096
        yaml.dump(self._metadata, bytes_io)
    
        byte_str = bytes_io.getvalue().decode('UTF-8')
        lines = byte_str.split('\n')
        
        if run_path is None:
            f_out_path = '_'.join([self.run_path, 'annotated'])
        else:
            f_out_path = '_'.join([run_path])
        
        with open(f_out_path, 'w') as f_out:
            
            f_out.write(''.join([META_START, '\n']))
            for line in lines[:-1]:
                f_out.write(' '.join(['#', line, '\n']))            
            f_out.write(''.join([META_END, '\n']))
            
            with open(self.run_path, 'r') as f_in:
                for run_line in f_in.readlines():
                    f_out.write(run_line)
                
    def complete_metadata(self, repo_path='.'):
        """
        This method automatically adds metadata about the Platform and 
        the Implementation component.
        
        @param repo_path: Path to the git repository of the Implementation that 
                          underlies the run file. If not specified this method
                          assumes that the program is executed from the root 
                          directory of the git repository.
        """
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
            
        if self._metadata.get('implementation') is None: 
            self._metadata['implementation'] = self._get_src(repo_path=repo_path)
    
    @staticmethod
    def strip_metadata(annotated_run):
        '''
        Strips off the metadata and returns a dict-version of the run that is parsed with pytrec_eval.
        
        @param annotated_run: Path to the annotated run file.
        
        @return: defaultdict that can be used with pytrec_eval or repro_eval.
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
        
        @param run_path: Path to the run file.
        
        @return: Dictionary containing the metadata information of the annotated 
                 run file.
        '''
        
        _metadata = None
        
        with open(run_path, 'r') as f_in: 
            lines = f_in.readlines()
            if lines[0].strip('\n') == META_START:
                metadata_str = ''
                yaml=YAML(typ='safe')

                for line in lines[1:]:
                    if line.strip('\n') != META_END:
                        metadata_str += line.strip('#')
                    else:
                        break
                _metadata = yaml.load(metadata_str)
        
        return _metadata
    
    @staticmethod
    def read_metadata_template(metadata_path):
        """
        This method reads in a YAML file containing the metadata.
        
        @param template_path: Path to the metadata YAML file.
        
        @return: Nested dictionary containing the metadata.
        """
        
        with open(metadata_path, 'r') as f_in:
            yaml = YAML(typ='safe')
            return yaml.load(f_in)

    def _get_cpu(self):
        """
        Reads out metadata information about the CPU including the model's name
        the architectures, the operation mode and the number of available cores.
        """
        
        cpu = cpuinfo.get_cpu_info()
        return {
            'model': cpu['brand_raw'],
            'architecture': platform.machine(),
            'operation mode': '-'.join([str(cpu['bits']), 'bit']),
            'number of cores': cpu['count'],
        }
      
    def _get_os(self):
        """
        Reads out metadata information about the operating system including 
        the platform (e.g. Linux), the kernel release version, 
        and the distribution's name.
        """
        
        try:
            with open("/etc/os-release") as f_in:
                os_info = {}
                for line in f_in:
                    k,v = line.rstrip().split('=')
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
        """
        Reads out the available RAM and returns the size in GB.
        """
        
        memory_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') 
        memory_gb = memory_bytes/(1024.0 ** 3)  
        return ' '.join([str(round(memory_gb, 2)),'GB'])

    def _get_libs(self):
        """
        Reads out all installed Python packages of the active environment.
        """
        
        installed_packages = [d.project_name for d in pkg_resources.working_set]
        return {'libraries': {'python': installed_packages}}

    def _get_src(self, repo_path='.'):
        """ 
        Reads out information from the specified repository.
        
        @param repo_path: Path to the git repository of the Implementation that 
                          underlies the run file. If not specified this method
                          assumes that the program is executed from the root 
                          directory of the git repository.        
        """
        
        extensions_path = pkg_resources.resource_filename(__name__, 'resources/extensions.json')

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
