<b>HashListConverter</b>

</br>将<a href="https://kts.sakaiweb.com/hashlister.html">HashLister</a>生成的txt文件（仅支持算法为SHA-1或MD5的“CRC list”格式）转换为用于Total Commander校验的sha或md5文件。

</br>仅支持单个txt文件的处理。
</br>支持拖放。
</br>输出目录默认与输入文件相同，无需选择。
</br>自动识别文本特征输出对应的校验文件（.sha或.md5）。
</br>支持处理<a href="https://goodbest.github.io/anime_hash/index.html">Anime hash保管库</a>中的文件列表（仅限SHA-1和MD5）。

</br><b>代码由GhatGPT生成。</b>

</br>需要以下系统环境：
</br>Python：确保在您的系统上安装了Python。您可以从<a href="https://www.python.org/downloads/">Python官方网站</a>下载并按照特定于您的操作系统的安装说明进行安装。

</br>必需的Python包：
</br>os：这个包是Python标准库的一部分，不需要额外安装。
</br>re：这个包是Python标准库的一部分，不需要额外安装。
</br>tkinter：这个包用于创建图形用户界面（GUI），大多数Python安装应该默认包含它。
</br>tkinterdnd2：这个包用于在GUI中启用拖放功能。您可以使用pip安装它，运行“<b>pip install tkinterdnd2</b>”。
</br>chardet：这个包用于检测文本文件的编码。您可以使用pip安装它，运行“<b>pip install chardet</b>”。

</br>在运行代码之前，请确保所有必需的包都已安装好。
