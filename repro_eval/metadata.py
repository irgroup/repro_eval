import os
from io import BytesIO, TextIOWrapper
from collections import defaultdict
from ruamel.yaml import YAML
from pytrec_eval import parse_run


class PrimadExperiment:
    def __init__(self, reference, type, reproductions):
        pass



class MetadataAnalyzer:
    def __init__(self, run_path):
        self.reference_run_path = run_path
        self.reference_run = MetadataHandler.strip_metadata(run_path)
        self.reference_metadata = MetadataHandler.read_metadata(run_path)
        
        
    def analyze_directory(self, dir_path):
        files = os.listdir(dir_path)
        
        primad_types = {}

        for _file in files:
            file_path = os.path.join(dir_path, _file)
            
            if file_path == self.reference_run_path:
                continue
            
            metadata = MetadataHandler.read_metadata(file_path)
            
            primad_str = ''
                                        
            for component in ['platform', 'research goal', 'implementation', 'method', 'actor', 'data']:
                if self.reference_metadata[component] != metadata[component]:
                    primad_str += component[0].upper()
                else:
                    primad_str += component[0]
            
            primad_types[file_path] = primad_str
            
        experiments = defaultdict(list)
        for k, v in primad_types.items(): 
            experiments[v].append(k)
            
        return experiments

    


class MetadataHandler:
    def __init__(self, run_path, metadata_path=None):
        
        self.run_path = run_path
        
        if metadata_path:
            self.metadata = MetadataHandler.read_metadata_file(metadata_path)
        else:
            self.metadata = MetadataHandler.read_metadata(run_path)
        
    def get_metadata(self):
        
        return self.metadata
    
    def set_metadata(self, metadata=None, metadata_path=None):
        
        if metadata_path:
            self.metadata = MetadataHandler.read_metadata_template(metadata_path)
        
        if metadata:
            self.metadata = metadata
    
    def dump_metadata(self, dump_path=None):
        
        if self.metadata:
        
            self.complete_metadata()
                
            tag = self.metadata['tag'] 
            f_out_name = '_'.join([tag, 'dump.yml'])  
            f_out_path = os.path.join(dump_path, f_out_name)    
                
            with open(f_out_path, 'wb') as f_out:
                bytes_io = BytesIO()
                yaml = YAML()
                yaml.dump(self.metadata, bytes_io)
                f_out.write(bytes_io.getvalue())

    def write_metadata(self, run_path=None):
        
        self.complete_metadata()
        
        bytes_io = BytesIO()
        yaml = YAML()
        yaml.dump(self.metadata, bytes_io)
    
        byte_str = bytes_io.getvalue().decode('UTF-8')
        lines = byte_str.split('\n')
        
        if run_path is None:
            f_out_path = '_'.join([self.run_path, 'annotated'])
        else:
            f_out_path = '_'.join([run_path, 'annotated'])
        
        with open(f_out_path, 'w') as f_out:
            
            f_out.write('# METADATA - START\n')
            for line in lines[:-1]:
                f_out.write(' '.join(['#', line, '\n']))            
            f_out.write('# METADATA - END\n')
            
            with open(self.run_path, 'r') as f_in:
                for run_line in f_in.readlines():
                    f_out.write(run_line)
                
    def complete_metadata(self):
        # TODO: Implement automatic completion of metadata
        pass
    
    @staticmethod
    def strip_metadata(annotated_run):
        """
        Strips off the metadata and returns a dict-version of the run that is parsed with pytrec_eval.
        """

        with TextIOWrapper(buffer=BytesIO(), encoding='utf-8', line_buffering=True) as text_io_wrapper:
            with open(annotated_run, 'r') as f_in:
                lines = f_in.readlines()
                for line in lines:
                    if line[0] != '#':
                        text_io_wrapper.write(line)
            text_io_wrapper.seek(0,0)        
            run = parse_run(text_io_wrapper)
                        
        return run

    @staticmethod
    def read_metadata(run_path):
        """
        Reads the metadata out of an annotated run and returns a dict containing the metadata.
        """
        
        metadata = None
        
        with open(run_path, 'r') as f_in: 
            lines = f_in.readlines()
            if lines[0].strip('\n') == '# METADATA - START':
                metadata_str = ''
                yaml=YAML(typ="safe")

                for line in lines[1:]:
                    if line.strip('\n') != '# METADATA - END':
                        metadata_str += line.strip('#')
                    else:
                        break
                metadata = yaml.load(metadata_str)
        
        return metadata
    
    @staticmethod
    def read_metadata_template(template_path):
        with open(template_path, "r") as f_in:
            yaml = YAML(typ='safe')
            return yaml.load(f_in)
