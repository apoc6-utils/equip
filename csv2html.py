import csv


def make_html(csvFilePath, htmlFilePath): 
      
    # create an array
    data = []
      
    # Open a csv reader called DictReader 
    with open(csvFilePath, encoding='utf-8') as csvf: 
        csvReader = csv.DictReader(csvf) 
        
        
        # Convert each row into a dictionary  
        # and add it to data 
        for row in csvReader: 
            
            
            #first column is primary key
            key = row['NAME'] 
            try:
                row["ML"] = int(row["ML"])
            except ValueError:
                pass
            try:
                row["AP"] = int(row["AP"])
            except ValueError:
                pass
            try:
                row["weight"] = int(row["weight"])
            except ValueError:
                pass
            try:
                row["value"] = int(row["value"])
            except ValueError:
                pass
            try:
                row["rent"] = int(row["rent"])
            except ValueError:
                pass
            
            row["ALIGN FLAGS"] = row["ALIGN FLAGS"].replace("f-g", "<span class=\"gCol\">f-g</span>")
            row["ALIGN FLAGS"] = row["ALIGN FLAGS"].replace("f-e", "<span class=\"eCol\">f-e</span>")
            row["ALIGN FLAGS"] = row["ALIGN FLAGS"].replace("f-n", "<span class=\"nCol\">f-n</span>")
            row["ALIGN RES"] = row["ALIGN RES"].replace("a-g", "<span class=\"gCol\">a-g</span>")
            row["ALIGN RES"] = row["ALIGN RES"].replace("a-e", "<span class=\"eCol\">a-e</span>")
            row["ALIGN RES"] = row["ALIGN RES"].replace("a-n", "<span class=\"nCol\">a-n</span>")
            row["FLAGS"] = row["FLAGS"].replace("breaks", "<span class=\"wCol\">breaks</span>")
            row["AVGD"] = row["AVGD"].replace(".0", "")

            data.append(row)
  
    
  
    # Open a json writer, and use the json.dumps()  
    # function to dump data 
    with open(htmlFilePath, 'w', encoding='utf-8') as htmlf:
        # TODO output beginning of web page
        htmlf.write('''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>apoc6 Equip</title>
  <link href="./css/apoc6eq.css" rel="stylesheet">
  <style id="col-visibility"></style>
</head>
<body>
  <div id="about">
	<div>
		<a href="#" title="Close" class="close">X</a>
		<h2>Apoc6 EquipDB Info</h2>
		<p>This is a db of equipment identified in apoc6. It is directly parsed from the in-game output, and reorganized into fields to provide a balance between search-ability (grouping similar stats) and usability (not too many columns). Features include:</p>
		<ul>
		  <li>filterable</li><li>show/hide columns</li><li>regular updates</li>
		</ul>
		<p>Downloads:</p>
		<ul>
		  <li><a href="a6-eq-parsed.csv" download>parsed (fields matching this page) csv file</a></li><li><a href="a6-eq-orig.csv" download>original (same fields as in-game) csv file</a></li>
		</ul>
		<p>Note: While somewhat responsive, this page is probably not mobile friendly, and given the data, does not lend itself to use on a mobile device.</p>
		<p>If you are interested in contributing to the database or find a problem with the website, contact Cahir/Fenor in apoc or discord.</p>
	</div>
  </div>
  <div id="table_container">
    <table id="apoc6_eq_table" class="apoc6eq">
      <caption>
        <h1>Apoc6 Eequipment</h1>
''')
        htmlf.write("        <span class=\"item-count\">(" + str(len(data)) + " items)</span>\n")
        htmlf.write('''        <div id="table-controls">
            <a class="button" href="#column-toggles">Toggle Columns</a><button onclick="clearFilters()">Clear Filters</button><a class="button" id="about-button" href="#about">About</a>
        </div>
        <div id="column-toggles">
            <a href="#" title="Close" class="close">X</a>
''')


        doHeader = True
        for row in data:
            if doHeader:
                #output table caption
                i = 1
                for field in row:
                    isChecked = " checked"
                    if i == 2 or i == 7 or i == 17 or i == 18 or i == 19 or i == 20 or i == 23 or i == 24 or i == 25 or i == 26 or i == 27:
                        isChecked = ""
                    displayName = field.title()
                    if i == 3:
                        displayName = "ML"
                    elif i == 15:
                        displayName = "AP"
                    elif i == 23:
                        displayName = "NoID"
                    
                    if i > 1:
                        htmlf.write("            <div class=\"checkbox\"><input onclick=\"toggleStylesheetRule(" + str(i) + ")\" type=\"checkbox\" value=\"" + str(i) + "\"" + isChecked + "><label>" + displayName + "</label></div>\n")
                    i = i + 1
                
                #output table header section
                htmlf.write("      </div>\n    </caption>\n    <thead>\n      <tr>\n")
                for field in row:
                    #if field.islower():
                        # do something to set initial visibility?
                    fieldClass = field.replace(" ", "-") + "-col"
                    htmlf.write("        <th class=\"center " + fieldClass + "\">" + field + "<br /><input class=\"filter\" onkeyup=\"filterTable()\"></th>\n")
                htmlf.write("      </tr>\n    </thead>\n")
                htmlf.write("    <tbody>\n")
                doHeader = False

            #output table body rows
            doRowHeader = True
            htmlf.write("      <tr>\n")
            for field in row:
                fieldClass = field.replace(" ", "-") + "-col"
                if doRowHeader:
                    htmlf.write("        <th class=\"" + fieldClass + "\"><div>" + row['NAME'] + "</div></th>\n")
                    doRowHeader = False
                else:
                    htmlf.write("        <td class=\"" + fieldClass + "\"><div>" + str(row[field]) + "</div></td>\n")
            htmlf.write("      </tr>\n")    
        htmlf.write("    </tbody>\n</table>\n")
        
        # TODO - output end of web page
        htmlf.write('''
  </div>
  <script type="text/javascript">
      function filterTable() {
        const query = q => document.querySelectorAll(q);
        const filters = [...query('th input')].map(e => new RegExp(e.value, 'i'));

        query('tbody tr').forEach(row => row.style.display = 
          filters.every((f, i) => f.test(row.cells[i].textContent)) ? '' : 'none');
      }
      
      var filterFields;
      window.onload = function() {
        filterFields = document.getElementsByClassName('filter');
        
        addStylesheetRules();
      }
      
      function addStylesheetRules() {
          var styleEl = document.getElementById('col-visibility');
          
          // Grab style element's sheet
          var styleSheet = styleEl.sheet;
          
          // create placeholder rule to align column numbers
          styleSheet.insertRule('.button {display:inline-block;}', styleSheet.cssRules.length);
          
          if (styleSheet.cssRules.length == 1) {
            // create rule for every column
            var currRule = '';
            for (var i = 1; i <= 27; i++) {
              if (i == 2 || i == 7 || i == 17 || i == 18 || i == 19 || i == 20 || i == 23 || i == 24 || i == 25 || i == 26 || i == 27) {
                currRule = '#apoc6_eq_table tr > *:nth-child(' + i + ') {display:none;}';
              } else {
                currRule = '#apoc6_eq_table tr > *:nth-child(' + i + ') {}';
              }
              styleSheet.insertRule(currRule, i);
            }
          }
      }
          
      function toggleStylesheetRule(colNum) {
          // Grab style element and sheet
          var styleEl = document.getElementById('col-visibility');
          var styleSheet = styleEl.sheet;
          
          // if rule exists
          if (colNum <= styleSheet.cssRules.length) {
              // get it and check for "none"
              var rule = styleSheet.cssRules[colNum];
              styleSheet.deleteRule(colNum);
              if (rule.cssText.includes('none')) {
                styleSheet.insertRule('#apoc6_eq_table tr > *:nth-child(' + colNum + ') {}', colNum);
              } else {
                styleSheet.insertRule('#apoc6_eq_table tr > *:nth-child(' + colNum + ') {display:none;}', colNum);
              }
          }
      }
      
      function clearFilters() {
        Array.prototype.forEach.call(filterFields, function(currFilter) {
            currFilter.value = '';
        });
    
        // refilter table
        filterTable();
      }
  </script>
</body>
</html>
''')
        
        htmlf.close()
        
          
# Driver
csvFilePath = pathlib.Path(__file__).parent / 'docs' / 'a6-eq-parsed.csv'
htmlFilePath = pathlib.Path(__file__).parent / 'docs' / 'index.html'
  
# Call the make_json function 
make_html(csvFilePath, htmlFilePath)



