from google import genai
class summerizer:
    client = genai.Client(api_key="AIzaSyBWBS1bgw7ojaCCsTqHXrnF27pcknqoXjo")
    
    def sum(self, list_selected_sorted, keyword):
        responseP = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[f"依照我給你的list，給我一些關於{keyword}的5個正面關鍵字，回傳內容請簡單、具體、扼要，格式為純文字，只回傳5個關鍵詞 詞語之間務必用空格分隔", list_selected_sorted]  
        )
        print("正面關鍵字：" + responseP.text)

        responseN = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[f"依照我給你的list，給我一些關於{keyword}的5個負面關鍵字，回傳內容請簡單、具體、扼要，格式為純文字，只回傳5個關鍵詞 詞語之間務必用空格分隔", list_selected_sorted]  
        )
        print("負面關鍵字："+responseN.text)

        responseS = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[f"依照我給你的list，給我一些關於{keyword}的結論，回傳格式純文字，結論長度5句話以內，語句通暢，同時術語盡量簡單好了解", list_selected_sorted]  
        )
        print(responseS.text)


