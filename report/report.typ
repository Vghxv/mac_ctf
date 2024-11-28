
#import "@preview/algo:0.3.3": algo, i, d, comment, code
// #import "@preview/tada:0.1.0"
#import "@preview/frame-it:1.0.0"
#set document(title: [Vulnerable MAC])
#set heading(numbering: "1.1")

#align(center, text(24pt)[
  Vulnerable MAC CTF Design Proposal and Implementation
])

#outline(
    depth: 2,
    title: "Table of contents",
    indent: 0.5cm
)

= Introduction

大部分的 MAC 是針對 fixed-length 訊息設計的。然而，有時候，我們需要對不同長度的訊息進行 MAC 驗證。在這種情況下，我們可以做 domain extension。常見的方法是將 message 分段，然後對每個分段進行 HMAC 或 NMAC 驗證。

let $pi$' = (Gen', Mac', Vrfy') be fixed length msg Mac. (n-bits)

let $pi$ = (Gen, Mac, Vrfy) be variable length msg Mac. (arbitrary length)

$G e n(n)$: identical to Gen'(n) $arrow.r$ k $in {0, 1}^n$

$M a c(k, m)$: k $in {0, 1}^n$, m $in {0, 1}^*$

$V r f y(k, m, t)$: k $in {0, 1}^n$, m $in {0, 1}^*$, t $in {0, 1}^n$

(i) Parse m into d blocks $(m_1, m_2, dots m_d)$ where each of length $frac(n,4)$. Note that the last one can be padded by 0s

(ii) choose a uniform r $in$ ${0,1}^frac(n,4)$

(iii) for i = 1, 2, $dots$ d, $t_i arrow.l$ $M a c_k$' $(r ||l||i||m_i)$, output $t = (r, t_1, dots t_d)$

過程中的 r, l, i 缺一則會使 MAC 變得不安全。


== Goal

利用缺少 r, l 或 i 的產生的漏洞設計 CTF。

= Implementation

使用者可以訪問一個生成給定訊息的 MAC 的 MAC oracle。該 MAC 是使用一個易受攻擊的 MAC 實現生成的(缺少 l )。使用者可以為尚未向 MAC oracle 查詢的訊息提交偽造的 MAC。如果 MAC 有效，伺服器將回應 flag。否則，伺服器將回應錯誤訊息。在 main page 上，使用者可以選擇性的查看 hint，以幫助他們得到 flag。

== Main Page

#figure(
    image("welcome.png", width: 100%),
    caption: "Main Page"
)

== Endpoints

/mac: 使用者可以訪問 MAC oracle 並提交訊息以獲取 MAC。

/submit: 使用者可以提交偽造的 MAC 以獲取 flag。
= Team Members

110590005 蕭耕宏

112C53035 王煥昇

113C53006 吳仲霖

113598043 張育丞

113598088 李以謙

= Links
// put this two images in the same row
#grid(
    columns: 2,     // 2 means 2 auto-sized columns
    gutter: 2mm,    // space between columns
    figure(
        image("repo.png", width: 50%),
        caption: link("https://github.com/Vghxv/mac_ctf")[Repository]
    ),
    figure(
        image("demo.png", width: 50%),
        caption: link("https://www.youtube.com/watch?v=eHS0DHxVstA")[Demo]
    ),
)
