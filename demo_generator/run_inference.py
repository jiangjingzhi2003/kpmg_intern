import argparse
import qianfan
from util import *

def parse_arguments(demo):
    parser = argparse.ArgumentParser(description="Zero-shot-CoT")

    parser.add_argument("--random_seed", type=int, default=1, help="random seed")
    parser.add_argument(
        "--dataset", type=str, default="elementary_math", choices=["elementary_math"], help="dataset used for experiment"
    )
    parser.add_argument(
        "--demo_path", type=str, default="demos/multiarith", help="pre-generated demos used for experiment"
    )
    parser.add_argument(
        "--resume_id", type=int, default=0, help="resume from which question id (current line number in the output file), if the experiment fails accidently (e.g., network error)"
    )
    parser.add_argument("--minibatch_size", type=int, default=1, choices=[1], help="minibatch size should be 1 because GPT-3 API takes only 1 input for each request")
    
    parser.add_argument("--max_num_worker", type=int, default=0, help="maximum number of workers for dataloader")
    
    parser.add_argument(
        "--model", type=str, default="wenxin", choices=["gpt-3.5-turbo","ERNIE-Bot"], help="model used for decoding. Note that 'gpt3' are the smallest models."
    )
    
    parser.add_argument(
        "--method", type=str, default="auto_cot", choices=["zero_shot", "zero_shot_cot", "few_shot", "few_shot_cot", "auto_cot"], help="method"
    )
    parser.add_argument(
        "--output_dir", type=str, default="experiment/elem_math", help="output directory"
    )
    parser.add_argument(
        "--max_length_cot", type=int, default=512, help="maximum length of output tokens by model for reasoning extraction"
    )
    parser.add_argument(
        "--max_length_direct", type=int, default=64, help="maximum length of output tokens by model for answer extraction"
    )
    parser.add_argument(
        "--limit_dataset_size", type=int, default=0, help="whether to limit test dataset size. if 0, the dataset size is unlimited and we use all the samples in the dataset for testing."
    )
    parser.add_argument(
        "--api_time_interval", type=float, default=1.0, help="sleep between runs to avoid excedding the rate limit of openai api"
    )
    parser.add_argument(
        "--temperature", type=float, default=0.000001, help="temperature for LLM"
    )
    parser.add_argument(
        "--log_dir", type=str, default="./log/", help="log directory"
    )
    
    args = parser.parse_args(["--dataset","elementary_math","--demo_path",f"demos/{demo}"])
    
    if args.dataset == "elementary_math":
        args.dataset_path = "../CMMLU/data/test/elementary_mathematics.csv"
        args.direct_answer_trigger = "\n所以，从选项A到选项D，答案是："
    else:
        raise ValueError("dataset is not properly defined ...")
        
    # "Therefore, the answer ..." -> "The answer ..."
    trigger = args.direct_answer_trigger.replace("\n所以, ", "")
    args.direct_answer_trigger_for_zeroshot = trigger[0].upper() + trigger[1:]
    args.direct_answer_trigger_for_zeroshot_cot = args.direct_answer_trigger
    args.direct_answer_trigger_for_fewshot = "答案是"
    args.cot_trigger = "让我们一步一步来思考, "
    
    return args

def run_inference_func(prompt):
    args = parse_arguments()
    
    num_q = 10

    # Initialize decoder class (load model and tokenizer) ...
    decoder = Decoder()
    
    print('*************************')

    x = "Q: "+ prompt + "\n" + "A:"
    complete_prompt =  demo_text + x + " " + args.cot_trigger

    # Answer experiment by generating text ...
    max_length = args.max_length_cot if "cot" in args.method else args.max_length_direct
    z = decoder.decode(args, complete_prompt, max_length) # use LLM to answer question

    print(complete_prompt + z)

    print("Answer is " + answers[i])
    print('*************************')
    
    return complete + z
        
    

        
