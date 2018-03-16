
通过歌手或者歌曲来下载百度音乐

前期准备

需要用到知识有：requests，正则表达式re，python3 多线程 python3.6.

由于官方将于2020年 不再维护python2.x 所以我们选择python3.6.

安装requests:

    pip install requests

python3多线程参考廖雪峰大神的教程：

分析百度音乐

在搜索栏输入 歌手，如刘德华

得到url：http://music.baidu.com/search?key=刘德华

选中一条播放，打开开发者工具，查看  Network 下的media 发现 

MP3的下载链接为：http://zhangmenshiting.qianqian.com/data2/music/c7e34c85f48a5988c2dea2a039d158a7/540310851/540310851.mp3?xcode=b474a3c89367fc43c6826868de970894

分析发现在ting?method 下发现了response 为jqueryP格式 发现

get 方式的请求为http://tingapi.ting.baidu.com/v1/restserver/ting?method=baidu.ting.song.play&format=jsonp&songid=歌曲信息

歌曲信息我们可以通过 上面的url 用正则取出。下面开始写我们的代码。

开始写代码

    import requests
    import json
    def get_mp3_by_sid(sid):
        '''通过song_id 下载mp3'''
        api='http://tingapi.ting.baidu.com/v1/restserver/ting?method=baidu.ting.song.play&format=jsonp&songid=%s'%sid
        response=requests.get(api)
        html=response.text #获取返回信息
        data=json.loads(html)#讲字符串转化为json格式
        title=data['songinfo']['title']
        author=data['songinfo']['author']
        album_title=data['songinfo']['album_title']
        mp3_url=data['bitrate']['file_link']
        with open('%s.mp3 '%title,'wb') as f:
            f.write(requests.get(mp3_url).content)



以上通过sid可以下载指定歌曲。但是我们怎么通过歌手来获取sid呢？我们通过上面的url 来爬取

    def get_songid_by_name(name):
        '''通过歌手获取歌曲信息song_id'''
        url='http://music.qianqian.com/search'
        data={
            'key':name
        }
        response=requests.get(url,params=data)
        html=response.text
        reg='&quot;sid&quot;:(.*?),'
        song_ids=re.findall(reg,html,re.S)
        #返回为列表
        return song_ids

接下来通过main函数来获取歌曲

    def main():
        for sid in get_songid_by_name('刘德华'):
            get_mp3_by_sid(sid)

但是每次只能取第一页的歌曲，并不完整，我们翻到第二页发现url变成了

http://music.baidu.com/search/song?s=1&key=%E5%88%98%E5%BE%B7%E5%8D%8E&start=20&size=20&third_type=0

查看分页发现有如下信息。

    page-navigator-hook page-navigator { pageNavigator:{ 'total':156, 'size':20, 'start':0, 'show_total':0, 'focus_neighbor':0 } }

这时我们想到可以用多线程来下载各个页面上的歌曲，先获取歌曲一共有几页

    def get_pagenumb(name):
        '''
        获取总页数
        :param name:
        :return: 返回页数
        '''
        url = 'http://music.qianqian.com/search'
        data = {
            'key': name
        }
        response = requests.get(url, params=data)
        html = response.text
        num=0
        reg="pageNavigator:{ 'total':(.*?), 'size':(.*?), 'start':0, 'show_total':0, 'focus_neighbor':0 }"
        for total,size in re.findall(reg,html,re.S):
            num=int(total)//int(size)
            if num >int(total)/int(size):
                num=num-1
        return num,int(size)

接下来就是通过页数，一个页面一个线程 开始获取歌曲了，当然不要忘记import  import threading

    def main(name):
        num , size=get_pagenumb(name)
        print(num,size)
        for i in range(num+1):
            print(i,size)
            start_size=i*size
            print(i,size)
            print('start_size:%s'%start_size)
            t=threading.Thread(target=start_donwload,args=(name,start_size))
            t.start()





