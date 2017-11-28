import pandas as pd
from collections import Counter

def get_response(input_str):
    '''
    Get the response output from input
    '''
    input_str = input_str.lower()
    input_words = input_str.split()
    hs_code_finder = ["hs","code"]
    hs_code_finder_part = ["hs","code","part"]
    charles_tool_use = ["charles","export","to"]
    part_no_details = ["about", "part"]
    export_engine_details = ["export","engine"]
    export_part_details = ["export", "part"]
    export_dwg_details = ["export", "drawing"]
    where_parts_used = ["models","part","used"]
    good_bye = ["bye","good day", "thank"]

    if all(x in input_str for x in hs_code_finder_part):
        # All data for app object id_Part
        data = pd.read_excel("rob/HTS_database.xlsx", sheetname="Data")
        product = input_words[-1]
        data_indexed = data.set_index("Part Number")
        hs_list = []
        for item, frame in data["Part Number"].iteritems():
            try:
                if all(x in str(frame).lower() for x in product):
                    matching = data.iloc[[item]]
                    hs_codes = matching["HS Code"].tolist()
                    hs_list.append(hs_codes[0])
            except:
                None
        if len(hs_list) > 0:
            count = Counter(hs_list)
            hs_out = count.most_common()[0][0]
            probability = (float((count.most_common()[0][1]))/(len(hs_list)))*100
            return "Your HS code could be "+str(hs_out)+" with probability of "+str(probability)+" %"
        else:
            return "No considerable match found, please try again with more queries or proper format."
    elif all(x in input_str for x in hs_code_finder):
        # All data for app object id_Part
        data = pd.read_excel("rob/HTS_database.xlsx", sheetname="Data")
        if "of" in input_str:
            product = input_words[(input_words.index("of")+1):]
        elif "for" in input_str:
            product = input_words[(input_words.index("for")+1):]
        else:
            product = input_words[-1]
        data_indexed = data.set_index("Nomenclature")
        hs_list = []
        for item, frame in data["Nomenclature"].iteritems():
            try:
                if all(x in str(frame).lower() for x in product):
                    matching = data.iloc[[item]]
                    hs_codes = matching["HS Code"].tolist()
                    hs_list.append(hs_codes[0])
            except:
                None
        if len(hs_list) > 0:
            count = Counter(hs_list)
            hs_out = count.most_common()[0][0]
            probability = (float((count.most_common()[0][1]))/(len(hs_list)))*100
            return "Your HS code could be "+str(hs_out)+" with probability of "+str(probability)+" %"
        else:
            return "No considerable match found, please try again with more queries."
    elif all(x in input_str for x in charles_tool_use):
        # what at the conditions to use tool ({})
        product = input_words[(input_words.index("export")+1)]
        if input_words[-1]=="?":
            destination = input_words[-2]
        else:
            destination = input_words[-1]
        tools_sheet = pd.ExcelFile("charles/tools.xlsx")
        tools_data = tools_sheet.parse("Main")
        data = tools_data.set_index("Tool Name")
        data.index = data.index.str.lower()
        try:
            product_data = data.loc[product][destination.title()]
            next = data.loc[product]["Conditions and Limitations"]
            print product_data
            if product_data=='X':
                first = "You can ship it to "+destination
                return first + ", But also know the following \n"+ next
            else:
                return "Sorry, you are not allowed. Please see these details too. \n"+ next
        except:
            return "Sorry, i was not able to understand you, please type 'helpme' for options"
    elif all(x in input_str for x in part_no_details):
        # tell me about this part #    
        all_parts = pd.read_excel("rob/All_Parts.xlsx", sheetname="Data")
        part_to_draw = pd.read_excel("rob/Part_to_Drawing_info.xlsx", sheetname="Part_Information")
        data_use = pd.read_excel("rob/Part_Uses.xlsx", sheetname="Data")
        part_num = input_words[-1].upper()
        try:
            # part details
            data = all_parts.set_index("Part Number")
            model = data.loc[part_num][0]
            nomenclature = data.loc[part_num][1]
            # dwg details
            data_dwg = part_to_draw.set_index("Part")
            dwg_no = data_dwg.loc[part_num][0]
            dwg_info = data_dwg.loc[part_num][1]
            # uses of part
            parts_uses = data_use[data_use["Part"] == part_num]
            product_lines_col = parts_uses["Product Line"]
            product_lines = list(set(product_lines_col.tolist()))
            product_lines_len = len(product_lines)
            start1 = "This part number is used in "+str(product_lines_len)+" product lines which are "
            if product_lines_len > 1:
                end1 = "{} and {}".format(", ".join(product_lines[:-1]), product_lines[-1])
            else:
                end1 = product_lines[0]
            # part no. used in how many Engine Models
            parts_uses_model = data_use[data_use["Part"] == part_num]
            Engine_col = parts_uses_model["Engine Model"]
            Engine_models = list(set(Engine_col.tolist()))
            Engine_models_len = len(Engine_models)
            start2 = "This part number is used in "+str(Engine_models_len)+" Engine_models, some of it are "
            if Engine_models_len > 4:
                end2 = "{} and {}".format(", ".join(Engine_models[-4:-1]), Engine_models[-1])
            elif Engine_models_len > 4:
                end2 = "{} and {}".format(", ".join(Engine_models[:-1]), Engine_models[-1])
            else:
                end2 = Engine_models[0]
            part_print = "This product is a "+nomenclature+ " which is used in "+model
            dwg_print = "\n\nThe drawing for it is "+dwg_no+" that is "+dwg_info
            use_print = "\n\n"+start1+end1
            model_print = "\n\n"+start2+end2
            return part_print+dwg_print+use_print+model_print
        except:
            return "Sorry, i was not able to understand you, please type 'helpme' for options"
    elif 0:
        # part no. to drawing id and description
        part_to_draw = pd.read_excel("rob/Part_to_Drawing_info.xlsx", sheetname="Part_Information")
        data = part_to_draw.set_index("Part")
        dwg_no = data.loc["1154M12P01"][0]
        info = data.loc["102A358P01"][1]
        print "The drawing for this part is "+dwg_no+" and description is "+info
    elif 0:
        # part no. used in how many product lines
        data_use = pd.read_excel("rob/Part_Uses.xlsx", sheetname="Data")
        parts_uses = data_use[data_use["Part"] == "1022T88P01"]
        product_lines_col = parts_uses["Product Line"]
        product_lines = list(set(product_lines_col.tolist()))
        product_lines_len = len(product_lines)
        start = "This part number is used in "+str(product_lines_len)+" product lines which are  "
        if product_lines_len > 1:
            end = "{} and {}".format(", ".join(product_lines[:-1]), product_lines[-1])
        else:
            end = product_lines[0]
        print start+end
    elif all(x in input_str for x in where_parts_used):
        # part no. used in how many Engine Models
        data = pd.read_excel("rob/Part_Uses.xlsx", sheetname="Data")
        part_num = input_words[(input_words.index("part")+1)].upper()
        try:
            parts_uses = data[data["Part"] == part_num]
            Engine_col = parts_uses["Engine Model"]
            Engine_models = list(set(Engine_col.tolist()))
            Engine_models_len = len(Engine_models)
            start = "The Part number "+part_num+" is used in "+str(Engine_models_len)+" Engine_models, some of it are  "
            if Engine_models_len > 4:
                end = "{} and {}".format(", ".join(Engine_models[-4:-1]), Engine_models[-1])
            elif Engine_models_len > 4:
                end = "{} and {}".format(", ".join(Engine_models[:-1]), Engine_models[-1])
            else:
                end = Engine_models[0]
            return start+end
        except:
            return "Sorry, i was not able to understand you, please type 'helpme' for options"
    elif all(x in input_str for x in export_engine_details):
        # Engine model no. used to get its jurisdiction, classification and exportability
        data = pd.read_excel("rob/Master_Engine_Table.xlsx", sheetname="Engine Models")
        data = data.set_index("Hardware Product Model")
        model_num = input_words[-1].upper()
        try:
            jurisdiction = data.loc[model_num][0]
            classification = data.loc[model_num][1]
            in_19_f_1 = data.loc[model_num][2]
            exportability = data.loc[model_num][3]
            return "This Engine model no."+str(model_num)+" comes under "+jurisdiction+" and has an exportability of "+exportability+" under classification number "+classification
        except:
            return "Sorry, i was not able to understand you, please type 'helpme' for options"
    elif all(x in input_str for x in export_dwg_details):
        # All data for app object id_drawing
        data = pd.read_excel("rob/Drawing_Tags.xlsx", sheetname="Data")
        data = data.set_index("App object Id")
        part_num = input_words[-1].upper()
        try:
            app_type = data.loc[part_num]
            app_type = app_type["App type"][0]
            obj_desc = data.loc[part_num]
            obj_desc = obj_desc["Object description"][0]
            exportability = data.loc[part_num]
            exportability = exportability["US export status"][0]
            classification = data.loc[part_num]
            classification = classification["US classification code"][0]
            return "This drawing no."+str(part_num)+" is "+obj_desc+" which is used in "+app_type+" and has an exportability of "+exportability+" under classification number "+classification
        except:
            return "Sorry, i was not able to find it, please enter drawing number again."
    elif all(x in input_str for x in export_part_details):
        # All data for app object id_Part
        data_app_part = pd.read_excel("rob/Part_Tags.xlsx", sheetname="Data")
        part_num = input_words[-1].upper()
        try:
            data_ap = data_app_part.set_index("App object Id")
            app_type = data_ap.loc[part_num][0]
            obj_desc = data_ap.loc[part_num][1]
            exportability = data_ap.loc[part_num][2]
            classification = data_ap.loc[part_num][3]
            return "This Part no."+str(part_num)+" is a "+obj_desc+" which is used in "+app_type+" and has an exportability of "+exportability+" under classification number "+classification
        except:
            return "Sorry, i was not able to understand you, please type 'helpme' for options"
    elif any(x in input_str for x in good_bye):
        return "Great then. See you..!!"
    elif "hi" in input_str:
        return "Hi. This is Charles, How can i help you today?"
    else:
        return "\
        Here are some things you can try:\
        \n1) Tell me something about part 2340582T23\
        \n2) what is hs code for washer\
        \n3) What is the HS code for part 1277M90G02\
        \n4) Charles, can i export crashplan to India ?\
        \n5) Tell me about something about part 00704-0845-0001\
        \n6) Things to know for export of model engine 7LM2500AA107G01\
        \n7) Provide me details for export of part 1275M68P01\
        \n8) Help me know details for export of drawing 1275M68\
        \n9) Tell me engine models where part 102A358P05 is used"
