# Web of Science Literature Classifier

**An efficient tool for processing, parsing, and categorizing plain `.txt` files of literature search results exported by the Web of Science (WoS).**

**一个高效的工具，用于处理、解析和分类从 Web of Science (WoS) 导出的文献检索结果的纯文本（`.txt`）文件。**

------

**主要功能 / Main Features**

**(1) 关键词分析 / Keyword Analysis**
- 统计所有文献中出现的关键词及其频率，展示关键词在不同年份的分布情况 / Statistics on keywords and their frequency in all literature. Demonstrate the distribution of keywords across years.
- 按年份展示关键词的使用趋势，识别热门研究主题 / Show keyword usage trends by year and identify popular research topics.
- 自动对相似关键词进行分组（基于相似度阈值），解决同一概念不同表达的问题 / Automatic grouping of similar keywords (based on similarity thresholds) to solve the problem of different expressions of the same concept.

**(2) 国家或地区分析 / Country or area analysis**
- 从作者地址中提取国家或地区信息，并统计科研成果数量 / Extract country or region information from author addresses, and statistics on the number of publications.
- 显示不同国家或地区随时间的发文趋势 / Showing trends in communications over time for different countries or areas.

**(3) 可视化和数据导出 / Visualization and data export**
- 将关键词统计数据导出为Excel文件 / Export keyword statistics to Excel file.
- 将国家统计数据导出为CSV文件 / Export country statistics to CSV file.
- 导出生成的图表为PNG、PDF或SVG格式 / Export generated charts to PNG, PDF or SVG format.

------

## Usage / 使用方法

### 1. Export plain .txt using WOS / 使用WOS导出.txt文件

- Export plain `.txt` file using any database from *Web Of Science*
  使用 `python` 运行脚本，或者执行生成的 `.exe` 文件。
-  Here is an example using the *Web Of Science Core Collection*
  这里以 *web of science 核心收藏* 为例

(1) When we have finished searching and screening the documents, click on “Platin text file” in the “Export” option. / 检索和筛选文献结束后，点击"Export"选项中的"Platin text file"


(2) Check the number of ranges we want to export and select the record contents / 选中想要导出的范围数量并选择记录内容


(3) When we choose to export content, we must select the export “keywords” and “source” options, it is recommended to select all. /  选择导出内容时必须选择导出 “关键词” 和 “来源” 等选项，建议全选。


(4) Export as a .txt file and save locally to computer / 导出为.txt文件，并保存到电脑本地

### 2. Open the Program / 打开程序

- Run the program using `python` or execute the generated `.exe` file.
  使用 `python` 运行脚本，或者执行生成的 `.exe` 文件。

### 3. Select Files / 选择文件

- Use the **"Browse"** button to select one or more `.txt` files exported from Web of Science.
  使用 **“Browse”** 按钮选择一个或多个从 Web of Science 导出的 `.txt` 文件。
- The selected files will be displayed in the list box. Duplicate files will be automatically ignored.
  所选文件会显示在列表框中，重复文件会被自动忽略。


### 4. Export Results / 导出结果

------

## Contributing / 贡献

Welcome contributions to this project!
欢迎任何形式的贡献！

- If you encounter issues, feel free to open an issue on GitHub.
  如果您遇到问题，请随时在 GitHub 上提交 issue。
- To contribute code, fork this repository, make your changes, and submit a pull request.
  如果您想贡献代码，请 fork 此仓库，完成修改后提交 pull request。

------

## License / 许可证

This project is licensed under the MIT License.
本项目基于 MIT 许可证发布。
