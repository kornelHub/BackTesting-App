report_template_part_1 = """<!DOCTYPE html>
<html>
<style>

.container {
  width:100%;
  height:200px;
}

.left_container {
  height:auto;
  width:auto;
  float:left;
  background-color: rgb(55,55,55);
  border-radius:10px 10px 10px 10px;
  margin-top: 15px;
  margin-bottom: 15px;
  margin-right: 15px;
  margin-left: 15px;
}

.right_container {
  display: flex;
  width:auto;
  overflow:hidden;
}

.right_container_plot {
  width:auto;
  height:1200px;
  background-color: rgb(55,55,55);
  overflow:hidden;
  margin-top: 15px;
  margin-left: 15px;
  border-radius:10px 10px 10px 10px;
}

.rule{
  height:300px;
  width: 100%;
  background-color: rgb(55,55,55);
  border-radius:10px 10px 10px 10px;
  display: inline-block;
  margin-top: 15px;
}

.rule:first-of-type{
  margin-right: 15px;
}

.label{
  background-color: rgb(70,70,70);
  font: 20pt 'MS Shell Dlg 2';
  color: rgb(255,255,255);
  border-radius:10px 10px 10px 10px;
  text-align: center;
  margin-top: 0px;
  margin-bottom: 0px;
  margin-right: 0px;
  margin-left: 0px;
}

.text_inside{
  font: 10pt 'MS Shell Dlg 2';
  color: rgb(255,255,255);
  white-space: pre-line;
  margin-right: 15px;
  margin-left: 15px;
}"""

def callback_function(html):
    return html

def generate_html_report_to_file(summary_page, html_of_graphs):
    html_of_graphs = "<div style='height:1200px;'>" + html_of_graphs[17:-14]

    report_template_part_2 = f"""
    </style>
    <body style='background-color:rgb(45,45,45);'>
    <div class='container'>
        <div class='left_container'>
           <p class='label'>Transactions</p>
           <p class='text_inside'>{summary_page.transactions_textBrowser.toPlainText()}</p>
        </div>

        <div class='right_container'>
          <div class='rule'>
            <p class='label'>Buy rule</p>
            <p class='text_inside'>{2137}</p>
          </div>
          <div class='rule'>
            <p class='label'>Sell rule</p>
            <p class='text_inside'>{42069}</p>
          </div>
        </div>

        <div class='right_container_plot'>
          <p class='label'>Plot</p>
            {html_of_graphs}
        </div>
    </div>
    </body>
    </html>"""

    f = open("data/reports/demofile3.html", "w")
    f.write(report_template_part_1 + report_template_part_2)
    f.close()