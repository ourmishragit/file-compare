#Python and Panda use for spread sheet comparison
#################################################
import gradio as gr
import pandas as pd
import os

from collections import defaultdict

cach_1 = pd.DataFrame()
cach_2 = pd.DataFrame()


def dataset_display(file1,file2):
    global cach_1
    global cach_2

    dict1 = defaultdict(list)
    dict2 = defaultdict(list)

    split_tup_1 = os.path.splitext(file1.name)
    split_tup_2 = os.path.splitext(file2.name)
  
    if (split_tup_1[1] and split_tup_2[1]) == '.xlsx' :
        try:
            df1=pd.read_excel(file1.name,dtype=str)
            for i in range(len(df1.index)):
                dict1[list(df1[i:i+1].ACCOUNT_NAME)[0]].append((list(df1[i:i+1]['ENTITLEMENT VALUE'])[0]))

            df2=pd.read_excel(file2.name,dtype=str)
            for i in range(len(df2.index)):
                dict2[list(df2[i:i+1].UNAME)[0]].append((list(df2[i:i+1].AGR_NAME)[0]))

        except:
            df1=pd.read_csv(file1.name,dtype=str)
            for i in range(len(df1.index)):
                dict1[list(df1[i:i+1].ACCOUNT_NAME)[0]].append((list(df1[i:i+1]['ENTITLEMENT VALUE'])[0]))

            df2=pd.read_csv(file2.name,dtype=str)
            for i in range(len(df2.index)):
                dict2[list(df2[i:i+1].UNAME)[0]].append((list(df2[i:i+1].AGR_NAME)[0]))
    
    # Output file1
    out1 = pd.DataFrame(list(dict1.items()),columns = ['ACCOUNT_NAME','ENTITLEMENT VALUE']) 

    # Output file2
    rows = []
    for item in list(out1.ACCOUNT_NAME):
        row = []
        row.append(item)
        row.append(dict2[item])
        rows.append(row)

    out2 = pd.DataFrame(rows,columns = ['UNAME','AGR_NAME'])
    
    cach_1 = out1
    cach_2 = out2

    return out1,out2

def export_csv():

    cach_1.to_csv("output1.csv")
    cach_2.to_csv("output2.csv")
    return gr.File.update(value="output1.csv", visible=True),gr.File.update(value="output2.csv", visible=True)

with gr.Blocks() as demo:
    gr.Markdown("# xlCompare ")

    with gr.Accordion(label="Instructions", open=False):
        gr.Markdown("""
        This Space matches information in two spreadsheets.
        following file format supported:
        - Only supporte files having extension .xlsx , .csv , .txt
        - Input File-1 / Campaign_SOX_Audit_Response should be having two columns named as 'ACCOUNT_NAME' & 'ENTITLEMENT VALUE'
        - Input File-2 / SA_SP1 should be having two columns named as 'AGR_NAME' & 'UNAME'
        """)
    with gr.Accordion(label="Limitations", open=False):
        gr.Markdown("""
        This tool should be treated as a Proof Of Concept, and is not designed for production-level use.
        - This is currently designed to only work [.xlsx , .csv , .txt] file types.
        - This tool relies on a very strict file schema, which may be different from your file schema.
    
        """)

    with gr.Tab("Upload the files"):
        gr.Markdown("##")
        with gr.Row():
            inp1 = gr.File(label="Input File-1 / Campaign_SOX_Audit_Response",file_types=['.xlsx','.csv','.txt'],interactive=True)
            inp2 = gr.File(label="Input File-2 / SA_SP1",file_types=['.xlsx','.csv','.txt'],interactive=True)

        with gr.Row():
            gen_btn = gr.Button(" File Compare ")

        with gr.Row():
            gen_btn_2 = gr.Button(" File Download ")
            csv1 = gr.File(interactive=False, visible=False)
            csv2 = gr.File(interactive=False, visible=False)

        with gr.Row():    
            gen_btn.click(
                dataset_display,
                inputs=[inp1,inp2],
                outputs=[gr.Dataframe(
                        label = "Processed File-1 / Campaign_SOX_Audit_Response",
                        headers=['UNAME', 'AGR_NAME'],
                        datatype=["str", "str"],
                        col_count=(2, "fixed"),
                        scroll_to_output= True,
                        show_progress = True
                ),
                        gr.Dataframe(
                        label = "Processed File-2 / SA_SP1",
                        headers=['ACCOUNT_NAME', 'ENTITLEMENT VALUE'],
                        datatype=["str", "str"],
                        col_count=(2, "fixed"),
                        scroll_to_output= True,
                        show_progress = True
                            )]
                            
            )
        gen_btn_2.click(export_csv, outputs=[csv1,csv2])

if __name__ == "__main__":
    demo.launch(server_name='0.0.0.0',server_port=7000)

