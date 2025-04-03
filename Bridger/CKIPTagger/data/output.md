[(2, {'公有': 2.0}), (3, {'土地公': 1.0, '土地婆': 1.0}), (5, {'緯來體育台': 1.0})]

'傅達仁今將執行安樂死，卻突然爆出自己 20 年前遭緯來體育台封殺，他不懂自己哪裡得罪到電視台。'
傅達仁(Nb)　今(Nd)　將(D)　執行(VC)　安樂死(Na)　，(COMMACATEGORY)　卻(D)　突然(D)　爆出(VJ)　自己(Nh)　 20(Neu)　年(Nf)　前(Ng)　遭(P)　緯來(Nb)　體育台(Na)　封殺(VC)　，(COMMACATEGORY)　他(Nh)　不(D)　懂(VK)　自己(Nh)　哪裡(Ncd)　得罪到(VJ)　電視台(Nc)　。(PERIODCATEGORY)　
(0, 3, 'PERSON', '傅達仁')
(18, 22, 'DATE', '20 年前')
(23, 28, 'ORG', '緯來體育台')

'美國參議院針對今天總統布什所提名的勞工部長趙小蘭展開認可聽證會，預料她將會很順利通過參議院支持，成為該國有史以來第一位的華裔女性內閣成員。'
美國(Nc)　參議院(Nc)　針對(P)　今天(Nd)　總統(Na)　布什(Nb)　所(D)　提名(VC)　的(DE)　勞工部長(Na)　趙小蘭(Nb)　展開(VC)　認可(VC)　聽證會(Na)　，(COMMACATEGORY)　預料(VE)　她(Nh)　將(D)　會(D)　很(Dfa)　順利(VH)　通過(VC)　參議院(Nc)　支持(VC)　，(COMMACATEGORY)　成為(VG)　該(Nes)　國(Nc)　有史以來(D)　第一(Neu)　位(Nf)　的(DE)　華裔(Na)　女性(Na)　內閣(Na)　成員(Na)　。(PERIODCATEGORY)　
(0, 2, 'GPE', '美國')
(2, 5, 'ORG', '參議院')
(7, 9, 'DATE', '今天')
(11, 13, 'PERSON', '布什')
(17, 21, 'ORG', '勞工部長')
(21, 24, 'PERSON', '趙小蘭')
(42, 45, 'ORG', '參議院')
(56, 58, 'ORDINAL', '第一')
(60, 62, 'NORP', '華裔')

''

'土地公有政策?？還是土地婆有政策。.'
土地公(Nb)　有(V_2)　政策(Na)　?(QUESTIONCATEGORY)　？(QUESTIONCATEGORY)　還是(Caa)　土地(Na)　婆(Na)　有(V_2)　政策(Na)　。(PERIODCATEGORY)　.(PERIODCATEGORY)　
(0, 3, 'PERSON', '土地公')

'… 你確定嗎… 不要再騙了……'
…(ETCCATEGORY)　 (WHITESPACE)　你(Nh)　確定(VK)　嗎(T)　…(ETCCATEGORY)　 (WHITESPACE)　不要(D)　再(D)　騙(VC)　了(Di)　…(ETCCATEGORY)　…(ETCCATEGORY)

'最多容納 59,000 個人,或 5.9 萬人,再多就不行了.這是環評的結論.'
最多(VH)　容納(VJ)　 59,000(Neu)　個(Nf)　人(Na)　,(COMMACATEGORY)　或(Caa)　 5.9 萬(Neu)　人(Na)　,(COMMACATEGORY)　再(D)　多(D)　就(D)　不行(VH)　了(T)　.(PERIODCATEGORY)　這(Nep)　是(SHI)　環評(Na)　的(DE)　結論(Na)　.(PERIODCATEGORY)　
(4, 10, 'CARDINAL', '59,000')
(14, 18, 'CARDINAL', '5.9 萬')

'科長說:1,坪數對人數為 1:3。2,可以再增加。'
科長(Na)　說(VE)　:1,(Neu)　坪數(Na)　對(P)　人數(Na)　為(VG)　 1:3(Neu)　。(PERIODCATEGORY)　 2(Neu)　,(COMMACATEGORY)　可以(D)　再(D)　增加(VHC)　。(PERIODCATEGORY)　
(4, 6, 'CARDINAL', '1,')
(12, 13, 'CARDINAL', '1')
(14, 15, 'CARDINAL', '3')
(16, 17, 'CARDINAL', '2')

CKIP Tagger 詞性標記說明
CKIP Tagger 輸出的標記如 VJ、VH 和 Neu 是詞性標記 (Part-of-Speech tags)，它們代表了詞語在句子中的語法功能。我來為您解釋這些標記的含義：

動詞相關標記
VJ (及物動詞)

意思：接受賓語的動詞
例子：「爆出」(VJ)、「得罪到」(VJ)、「容納」(VJ)
特點：這類動詞後面通常會有一個受詞（賓語）
VH (狀態不及物動詞)

意思：表示狀態的不及物動詞
例子：「順利」(VH)、「不行」(VH)、「最多」(VH)
特點：描述主語的狀態，通常不需要賓語
VHC (狀態使動動詞)

意思：使某事物產生某種狀態
例子：「增加」(VHC)
特點：使役意味的狀態動詞
數量詞標記
Neu (數詞)

意思：表示數量的詞
例子：「20」(Neu)、「59,000」(Neu)、「5.9 萬」(Neu)、「第一」(Neu)
特點：表示數量、序數或基數
其他常見詞性標記
Na: 普通名詞，如「政策」(Na)、「安樂死」(Na)
Nb: 專有名詞，如「傅達仁」(Nb)、「布什」(Nb)
Nc: 地方詞，如「美國」(Nc)、「電視台」(Nc)
Nd: 時間詞，如「今」(Nd)、「今天」(Nd)
Nh: 代名詞，如「自己」(Nh)、「他」(Nh)、「你」(Nh)
D: 副詞，如「將」(D)、「卻」(D)、「突然」(D)
DE: 的、之、得，如「的」(DE)
V_2: 有字，如「有」(V_2)
VC: 動作動詞，如「執行」(VC)、「封殺」(VC)
VK: 狀態動詞，如「懂」(VK)、「確定」(VK)
標點符號標記
COMMACATEGORY: 逗號
PERIODCATEGORY: 句號
QUESTIONCATEGORY: 問號
ETCCATEGORY: 省略號
完整詞性標記列表
CKIP Tagger 採用的是中央研究院中文詞庫小組開發的詞類標記系統，完整的標記系統非常詳細，大約有 100 多種詞性標記。

這些詞性標記對於語法分析、資訊擷取和自然語言理解任務都非常重要，它們讓我們能更精確地理解文本中每個詞的語法功能和語義角色。

要記住所有標記可能有些困難，但掌握常用的幾類標記（如動詞 V 開頭、名詞 N 開頭、副詞 D 開頭）會對理解 CKIP Tagger 的輸出很有幫助。