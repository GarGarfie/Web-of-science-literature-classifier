# Web of Science Literature Classifier

**An efficient tool for processing, parsing, and categorizing plain `.txt` files of literature search results exported by the Web of Science (WoS).**

**一个高效的工具，用于处理、解析和分类从 Web of Science (WoS) 导出的文献检索结果的纯文本（`.txt`）文件。**

------

## Features / 功能

- **Batch Processing / 批量处理**:
  Support for multi-file batch processing, allowing users to process multiple `.txt` files simultaneously.
  支持多文件批量处理，允许用户同时处理多个 `.txt` 文件。
- **Keyword Classification / 关键词分类**:
  Automatically classifies literature based on keywords contained in the articles.
  根据文章中包含的关键词自动对文献进行分类。
- **Statistical Analysis / 统计分析**:
  Generates year-by-year quantitative statistics for all exported literature.
  生成所有导出文献的逐年定量统计数据。
- **Excel Export / Excel 导出**:
  Exports the processed results and statistics to an Excel file.
  将处理结果和统计数据导出到 Excel 文件。

------

## Usage / 使用方法

### 1. Export plain .txt using WOS / 使用WOS导出.txt文件

- Export plain `.txt` file using any database from *Web Of Science*
  使用 `python` 运行脚本，或者执行生成的 `.exe` 文件。
-  Here is an example using the *Web Of Science Core Collection*
  这里以 *web of science 核心收藏* 为例

(1) When we have finished searching and screening the documents, click on “Platin text file” in the “Export” option. / 检索和筛选文献结束后，点击"Export"选项中的"Platin text file"

![Web-of-science-export-1.png](https://www.helloimg.com/i/2025/01/07/677c4c9339b55.png)

(2) Check the number of ranges we want to export and select the record contents / 选中想要导出的范围数量并选择记录内容

![Web-of-science-literature-classifier-2.png](https://www.helloimg.com/i/2025/01/07/677c4e824c001.png)

(3) When we choose to export content, we must select the export “keywords” and “source” options, it is recommended to select all. /  选择导出内容时必须选择导出 “关键词” 和 “来源” 等选项，建议全选。

![Web-of-science-literature-classifier-3.png](https://www.helloimg.com/i/2025/01/07/677c4f2a213a6.png)

(4) Export as a .txt file and save locally to computer / 导出为.txt文件，并保存到电脑本地

### 2. Open the Program / 打开程序

- Run the program using `python` or execute the generated `.exe` file.
  使用 `python` 运行脚本，或者执行生成的 `.exe` 文件。

### 3. Select Files / 选择文件

- Use the **"Browse"** button to select one or more `.txt` files exported from Web of Science.
  使用 **“Browse”** 按钮选择一个或多个从 Web of Science 导出的 `.txt` 文件。
- The selected files will be displayed in the list box. Duplicate files will be automatically ignored.
  所选文件会显示在列表框中，重复文件会被自动忽略。

### 4. Process Files / 处理文件

- Click the **"Process Files"** button to start processing the selected `.txt` files.
  单击 **“Process Files”** 按钮开始处理所选 `.txt` 文件。

### 5. Export Results / 导出结果

- Once the processing is complete, click the **"Export to Excel"** button to save the results to an Excel file.
  处理完成后，点击 **“Export to Excel”** 按钮，将结果保存到 Excel 文件中。

- The Excel file will contain two sheets:

  Excel 文件包含两个工作表：

  1. **Articles**: Processed articles with their titles, years, and keywords.
     **Articles**：包含文章标题、年份和关键词的处理结果。
  
  2. **Statistics**: Year-by-year keyword statistics.
     **Statistics**：逐年的关键词统计数据。
  

------

## Contributing / 贡献

We welcome contributions to this project!
我们欢迎任何形式的贡献！

- If you encounter issues, feel free to open an issue on GitHub.
  如果您遇到问题，请随时在 GitHub 上提交 issue。
- To contribute code, fork this repository, make your changes, and submit a pull request.
  如果您想贡献代码，请 fork 此仓库，完成修改后提交 pull request。

------

## License / 许可证

This project is licensed under the MIT License.
本项目基于 MIT 许可证发布。
