from PySide2 import QtCore
from engine.simulation import check_if_parent_exist

report_template_part_1 = """<!DOCTYPE html>
<html>
<style>

.container {
  width:100%;
  height:200px;
}

.left_container {
  height:1350px;
  width:auto;
  float:left;
  background-color: rgb(55,55,55);
  border-radius:10px 10px 10px 10px;
  margin-top: 15px;
  margin-bottom: 15px;
  margin-right: 15px;
  margin-left: 15px;
  overflow-y:auto
}

.right_container {
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
  background-color: rgb(55,55,55);
  border-radius:10px 10px 10px 10px;
  display: inline-block;
  margin-top: 15px;
  vertical-align: top;
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
  display: inline-block;
  font: 10pt 'MS Shell Dlg 2';
  color: rgb(255,255,255);
  white-space: pre-line;
  margin-right: 15px;
  margin-left: 15px;
}

    </style>
    <body style='background-color:rgb(45,45,45);' onload='adjust_rule_size();'>
    <script>
    function adjust_rule_size() {
      var buy_rule_width = document.getElementById('buy_rule').clientWidth
      var sell_rule_width = document.getElementById('sell_rule').clientWidth
      if (buy_rule_width > sell_rule_width) {
        document.getElementById('sell_rule').style.width=buy_rule_width.toString().concat('px')
      } else {
        document.getElementById('buy_rule').style.width=sell_rule_width.toString().concat('px')
      }

      var buy_rule_id_width = document.getElementById('buy_rule_id').clientWidth
      var sell_rule_id_width = document.getElementById('sell_rule_id').clientWidth
      if (buy_rule_id_width > sell_rule_id_width) {
        document.getElementById('sell_rule_id').style.width=buy_rule_id_width.toString().concat('px')
      } else {
        document.getElementById('buy_rule_id').style.width=sell_rule_id_width.toString().concat('px')
      }
      
      var buy_rule_id_height = document.getElementById('buy_rule_id').clientHeight
      var sell_rule_id_height = document.getElementById('sell_rule_id').clientHeight
      if (buy_rule_id_height > sell_rule_id_height) {
        document.getElementById('sell_rule_id').style.height=buy_rule_id_height.toString().concat('px')
      } else {
        document.getElementById('buy_rule_id').style.height=sell_rule_id_height.toString().concat('px')
      }
    }
</script>
"""

def generate_html_report_to_file(summary_page, html_of_graphs):
    html_of_graphs = "<div style='height:1200px;'>" + html_of_graphs[17:-14]

    buy_rules = summary_page.buy_rules_treeWidget.findItems('', QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive, 0)
    # buy_rules_id = summary_page.buy_rules_treeWidget.findItems('', QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive, 1)
    buy_rules_text = ''
    buy_rules_id_text = ''

    sell_rules = summary_page.sell_rules_treeWidget.findItems('', QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive, 0)
    # sell_rules_id = summary_page.sell_rules_treeWidget.findItems('', QtCore.Qt.MatchContains | QtCore.Qt.MatchRecursive, 1)
    sell_rules_text = ''
    sell_rules_id_text = ''


    for x in buy_rules:
        buy_rules_text += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'* check_if_parent_exist(x, 0) + x.text(0) + '\n'
        buy_rules_id_text += '| '+x.text(1) + '\n'


    for x in sell_rules:
        sell_rules_text += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'* check_if_parent_exist(x, 0) + x.text(0) + '\n'
        sell_rules_id_text += '| '+x.text(1) + '\n'

    transaction_text = summary_page.transactions_textBrowser.toPlainText().replace('      ', '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;')
    # transaction_text = transaction_text.replace('-'*76, '-'*20)
    print(transaction_text)

    report_template_part_2 = f"""
    <div class='container'>
        <div class='left_container'>
           <p class='label'>Transactions</p>
           <p class='text_inside'>{transaction_text}</p>
        </div>

        <div class='right_container'>
          <div class='rule'>
            <p class='label'>Buy rule</p>
            <p class='text_inside' id='buy_rule'>{buy_rules_text}</p>
            <p class='text_inside' id='buy_rule_id'>{buy_rules_id_text}</p>
          </div>
          <div class='rule'>
            <p class='label'>Sell rule</p>
            <p class='text_inside' id='sell_rule'>{sell_rules_text}</p>
            <p class='text_inside' id='sell_rule_id'>{sell_rules_id_text}</p>
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