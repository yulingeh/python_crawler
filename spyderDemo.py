import  requests
import  re
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0",}
url = 'http://www.jingcaiyuedu.com/book/15401.html'
#模拟浏览器发送一个请求
response = requests.get(url, headers=headers) #headers作用不清
response.encoding='utf-8'
#目标小说主页源码
html = response.text
#目标小说名字
book_title = re.findall(r' <meta property="og:title" content="(.*?)"/>',html)[0]
#新建文件保存小说内容
fp = open("%s.txt" %book_title,'w',encoding='utf-8')

#print(html)
#获取每一章节href对应的url
dl = re.findall(r'<dl class="panel-body panel-chapterlist">.*?</dl>',html,re.S)[1]  #只提取章节对应的url
aills = re.findall(r'href="(.*?)">(.*?)<',dl)

#循环每一个章节，分别下载内容
for aill in aills:
    chapter_info = aill[1]
    chapter_url = aill[0]
    chapter_url = "http://www.jingcaiyuedu.com%s" %chapter_url
    #print (chapter_url,chapter_info)
    #下载章节内容，request内容
    chapter_response = requests.get(chapter_url,headers = headers)
    chapter_response.encoding = 'utf-8'
    chapter_html = chapter_response.text
    #提取文字
    try:
        chapter_content = re.findall(r'<div class="panel-body" id="htmlContent">(.*?)</div>',chapter_html,re.S)[0]
    except IndexError:
        continue
    #将空格替换为空
    chapter_content = chapter_content.replace(' ','')
    #字符串替换为空
    chapter_content = chapter_content.replace('&nbsp', '')
    #将html的换行改成空
    chapter_content = chapter_content.replace('<br/>', '')
    #其他替换
    chapter_content = chapter_content.replace(';;;;', '')
    chapter_content = chapter_content.replace('书友们，我是讲古书生，推荐一个小说公众号,'
                                              '小蚂蚁追书，支持小说下载、听书、零广告、多种阅读模式。'
                                              '请您关注微信公众号：xiaomayizhuishu（长按三秒复制）'
                                              '书友们快关注起来吧！','')
    chapter_content = chapter_content.replace('<p>', '')
    chapter_content = chapter_content.replace('</p>', '')
    chapter_content = chapter_content.replace('ps：官方群号：219863813。欢迎各位兄弟姐妹们加入！！', '')
    #替换空格为空
    chapter_content = chapter_content.replace('\n', '')

    #print(chapter_content)
    fp.write(book_title)
    fp.write(chapter_content)
    fp.write('\n')
    print(chapter_url)

