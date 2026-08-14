
import os


class S3Sync:
    def sync_folder_to_s3(self,folder,aws_bucket_url):
        command = f"aws s3 sync {folder} {aws_bucket_url} "
        os.system(command)

    def sync_folder_from_s3(self,folder,aws_bucket_url):
        command = f"aws s3 sync  {aws_bucket_url} {folder} "
        os.system(command)

    def get_latest_model_from_s3(self, bucket_name: str) -> tuple[bool, str]:
        """
        Lists the final_model/ directory in S3, finds the latest timestamp folder,
        and syncs its contents to the local final_model/ directory.
        Returns (success: bool, message: str)
        """
        import subprocess
        from datetime import datetime
        try:
            result = subprocess.run(["aws", "s3", "ls", f"s3://{bucket_name}/final_model/"], capture_output=True, text=True)
            
            if result.returncode != 0:
                return False, f"AWS CLI Error: {result.stderr.strip()}"

            folders = []
            for line in result.stdout.split('\n'):
                if 'PRE' in line:
                    folder_name = line.strip().split()[-1].strip('/')
                    folders.append(folder_name)
            
            if not folders:
                return False, "No models found in the S3 bucket's final_model/ directory."
                
            def parse_ts(ts_str):
                try:
                    return datetime.strptime(ts_str, "%m_%d_%Y_%H_%M_%S")
                except:
                    return datetime.min
            
            latest_folder = max(folders, key=parse_ts)
            
            aws_bucket_url = f"s3://{bucket_name}/final_model/{latest_folder}/"
            self.sync_folder_from_s3(folder="final_model", aws_bucket_url=aws_bucket_url)
            return True, f"Successfully synced {latest_folder}"
        except Exception as e:
            return False, f"Exception occurred: {str(e)}"
