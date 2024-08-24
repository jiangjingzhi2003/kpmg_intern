import qianfan
import os
import pandas as pd
import json
import qianfan

os.environ["QIANFAN_AK"] = "vtPwTlnPvgIdb4DRSuyNDuIN"
os.environ["QIANFAN_SK"] = "Sp8CCvNsQgUsRKlJozQwWVClRliZ2S8m"
chat_comp = qianfan.ChatCompletion()



class Decoder():
    def __init__(self):
        # print_now()
        pass
 
    def decode(self, args, input, max_length):
        response = decoder_for_llm(args, input, max_length)
        return response
    
    
def decoder_for_llm(args,input,max_length):
    if args.model == "wenxin":
        engine = "ERNIE-Speed-128K"
    
    response = chat_comp.do(
                model=engine,
                messages=[{"role": "user", "content": input}],
                max_output_tokens=max_length,
                temperature=args.temperature,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                stop= None
            )
    return response.body["result"]


# create example COT demos text
def create_demo_text(args, cot_flag):
    x, z, y = [], [], []
    
    with open(args.demo_path, encoding="utf-8") as f:
        json_data = json.load(f)
        json_data = json_data["demo"]
        for line in json_data:
            x.append(line["question"])
            z.append(line["rationale"])
            y.append(line["pred_ans"])

    index_list = list(range(len(x)))
    
    demo_text = ""
    for i in index_list:
        if cot_flag:
            demo_text += x[i] + " " + z[i] + " " + \
                         args.direct_answer_trigger_for_fewshot + " " + y[i] + ".\n\n"
        else:
            demo_text += x[i] + " " + args.direct_answer_trigger_for_fewshot + " " + y[i] + ".\n\n"
    return demo_text

# load test_data and turn each column as a list for further formatting
def load_test_data(data_path):
    test_data = pd.read_csv(data_path)
    columns_as_lists = {col: test_data[col].tolist() for col in test_data.columns}
    
    return columns_as_lists

def initial_prompt_per_question(num, columns_as_lists):
    
    question = columns_as_lists['Question'][num]
    op_A = columns_as_lists['A'][num]
    op_B = columns_as_lists['B'][num]
    op_C = columns_as_lists['C'][num]
    op_D = columns_as_lists['D'][num]
    full_prompt = f"{question}\n A {op_A} \n B {op_B} \n C {op_C} \n D {op_D}"
    question_only = f"{question}"
    options = f"A {op_A} \n B {op_B} \n C {op_C} \n D {op_D}"
    return full_prompt, question_only, options

# create auto-cot prompt for one question
def auto_cot_prompt(args, num):
    columns_as_lists  = load_test_data(args.data_path)
    question = initial_prompt_per_question(num, columns_as_lists)
    demo_text = create_demo_text(args, cot_flag=True)
    
    complete_prompt = x = demo_text + x + " " + args.cot_trigger
    
    return complete_prompt