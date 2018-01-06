### 1 通过F4添加报头信息方法  /etc/vimrc
在脚本末尾添加如下信息即可
```
"add by peter for update in header
map <F4> ms:call AddAuthor()<cr>'s
function AddAuthor()

        let n=1

        while n < 5

                let line = getline(n)

                if line =~'^\s*\*\s*\S*Last\s*modified\s*:\s*\S*.*$'

                        call UpdateTitle()

                        return

                endif

                let n = n + 1

        endwhile

        call AddTitle()

endfunction
function UpdateTitle()

        normal m'

        execute '/* Last modified\s*:/s@:.*$@\=strftime(": %Y-%m-%d %H:%M")@'

        normal "

        normal mk

        execute '/* Filename\s*:/s@:.*$@\=": ".expand("%:t")@'

        execute "noh"

        normal 'k

        echohl WarningMsg | echo "Successful in updating the copy right." | echohl None

endfunction
function AddTitle()

        call append(0,"/**********************************************************")

        call append(1," * Author        : 作者")

        call append(2," * Email         : 邮箱地址")

        call append(3," * Last modified : ".strftime("%Y-%m-%d %H:%M"))

        call append(4," * Filename      : ".expand("%:t"))

        call append(5," * Description   : ")

        call append(6," * *******************************************************/")

        echohl WarningMsg | echo "Successful in adding the copyright." | echohl None

endfunction



```


### 2 :示例

```
[root@mgt1 ~]# vim peter.abc
/**********************************************************
 * Author        : 作者
 * Email         : 邮箱地址
 * Last modified : 2018-01-06 05:44
 * Filename      : peter.abc
 * Description   :
 * *******************************************************/

~



```

### 3 :通过~/.vimrc来实现脚本添加信息方法
```
[root@mgt1 ~]# cat /root/.vimrc
autocmd BufNewFile *.py,*.sh, exec ":call SetTitle()"
let $author_name = "Peter CZ Peng"
let $author_email = "pengcz1@lenovo.com"

func SetTitle()
if &filetype == 'sh'
call setline(1,"\#!/bin/bash")
call append(line("."), "\# File Name: ".expand("%"))
call append(line(".")+1, "\# Author: ".$author_name)
call append(line(".")+2, "\# mail: ".$author_email)
call append(line(".")+3, "\# Created Time: ".strftime("%c"))
call append(line(".")+4, "\#=============================================================")
call append(line(".")+5, "\#Description: this is a Bash Scripts for : ")
call append(line(".")+6, "")
else
call setline(1,"\###################################################################")
call append(line("."), "\# File Name: ".expand("%"))
call append(line(".")+1, "\# Author: ".$author_name)
call append(line(".")+2, "\# mail: ".$author_email)
call append(line(".")+3, "\# Created Time: ".strftime("%c"))
call append(line(".")+4, "\#=============================================================")
call append(line(".")+5, "\#!/usr/bin/python")
call append(line(".")+6, "")
endif
endfunc

```

### 4 :示例 

```
[root@mgt1 ~]# vim peter.sh
#!/bin/bash
# File Name: peter.sh
# Author: Peter CZ Peng
# mail: pengcz1@lenovo.com
# Created Time: Sat 06 Jan 2018 05:44:07 AM EST
#=============================================================
#Description: this is a Bash Scripts for :

~

```

