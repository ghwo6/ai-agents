import os,json,sys
import prompt_utils


def list_text_files_in_directory(directory):
    # text_files에 빈 리스트로 초기화
    text_files = []

    # directory에 대해 listdir을 함 (파일, 폴더들 나타냄)
    for filename in os.listdir(directory):
        # _ 로 시작하는 파일은 건너 띈다.
        if filename.startswith('_'):
            continue
        # jsonl로 끝나는 파일은 text_files에 추가한다.
        if filename.endswith(".jsonl"):
            text_files.append(filename)
    return text_files

def load_and_parse_json_file(file_path):
    # 데이터는 빈 리스트로 초기화 한다.
    data = []

    with open(file_path,"r",encoding="utf-8") as file:

        # json_text도 빈값으로 초기화 한다.
        json_text = ""
        # 파일에서 한줄씩 읽어 line에 대입
        # file이 제터레이터 형식으로 작동되기어 "\n" 을 만나는 지점까지 가져온다.
        
        for line in file:

            # line을 깔끔하게 strip()하고 가져온다.
            line = line.strip()

            # json_text에 line을 추가한다.
            json_text += line
            # "]"를 만나면 json_text를 json으로 로드한다.
            #  jsonl이라서 ] 이 json의 마지막 내용
            # json으로 바꾼내용을 data에 리스트로 어펜드 한다.
            if line == "]":
                try:
                    json_data = json.loads(json_text)
                    data.append(json_data)

                # 디코딩 에러가 발생하면 이를 에러처리한다.
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {json_text}")
                    print(e)
                json_text = ""
    return data

def main():
    origin_directory = os.path.dirname(__file__)
    
    # output폴더를 만들기로 함
    output_txt_folderName = "output"
    output_txt_folder_path = os.path.join(origin_directory,output_txt_folderName)
    if not os.path.exists(output_txt_folder_path):
        os.mkdir(output_txt_folder_path)
    

    directory = "prompts"  # You can change this to the directory containing your text files
    text_files = list_text_files_in_directory(os.path.join(origin_directory,directory))

    if not text_files:
        print("No Text Files found in the directory.")
        return
    
    def print_available():
        print("Available prompt tactics : ")
        for i, filename in enumerate(text_files,start=1):
            print(f"{i}, {filename}")
    
    while True:
        try:
            print_available()
            choice = int(input("Enter the number of the prompt tactic to run (or 0 to exit): "))
            if choice == 0:
                break
            elif 1 <= choice <= len(text_files):
                selected_file = text_files[choice -1]
                file_path = os.path.join(origin_directory,directory,selected_file)
                prompts = load_and_parse_json_file(file_path)
                print(f"Running prompts for {selected_file}")
                
                output_txt_fileName = os.path.basename(file_path) + ".txt"
                output_txt_file = os.path.join(origin_directory,directory,output_txt_fileName)
                
                with open(output_txt_file,"at",encoding="utf-8") as f:

                    for i,prompt in enumerate(prompts):
                        print(f"PROMPT {i+1} ---------------")
                        print(prompt)
                        print(f"REPLY ------------------------------")
                        # usingOpenAI
                        # print(prompt_utils.prompt_llm(prompt))
                        # 이부분 수정 base_url 등 등
                        result = prompt_utils.prompt_llm_modified(prompt)
                        print(result)
                        f.writelines(result+"\n")
                        # using Local LLM
                        # print(prompt_utils.prompt_llm(prompt,model="local-model",base_url="http://localhost:1234/v1",api_key="not_used"))
                
            else:
                print("Invalid choice. Please enter a valid number.")
        except KeyboardInterrupt:
            print("ctrl + c가 입력되었습니다.")
            sys.exit(1)
        except EOFError:
                print("EOF error -> 'ctrl + D'로 긴급탈출 합니다.")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    # for filename in os.listdir("./"):
    #     print(filename)
    main()
