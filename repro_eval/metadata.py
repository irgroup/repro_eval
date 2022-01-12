from io import BytesIO, TextIOWrapper
from ruamel.yaml import YAML
from pytrec_eval import parse_run

class MetadataWriter:
    def __init__(self, run_path, template_path):
        
        self.run_path = run_path
        
        with open(template_path, "r") as f_in:
            yaml = YAML(typ='safe')
            self.metadata = yaml.load(f_in)
    
    def get_metadata(self):
        
        return self.metadata
    
    def set_metadata(self, metadata):
        
        self.metadata = metadata
    
    def dump_metadata(self, dump_name=None):
        
        self.complete_metadata()
              
        f_out_name = self.metadata['tag'] if dump_name is None else dump_name
        with open('_'.join([f_out_name,'dump.yml']), 'wb') as f_out:
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


class MetadataReader:
    def __init__(self):
        pass
    
    def strip_metadata(self, annotated_run):
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

    
    def read_metadata(self, run_path):
        """
        Reads the metadata out of an annotated run and returns a dict containing the metadata.
        """
        
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
                