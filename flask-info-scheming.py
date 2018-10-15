
#!flask/bin/python
import json
import git
from flask import Flask, request, abort
from lookml import lookml, View, Dimension, DimensionGroup

app = Flask(__name__)

lookml.DB_FIELD_DELIMITER_START = ''
lookml.DB_FIELD_DELIMITER_END = ''

filename = 'generating_schema.view.lkml'
git_repo = 'git@github.com:bryan-at-looker/info_scheming.git'
git_dir = 'info_scheming'

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
      print(request.json)
      payload = request.json

      data = payload['attachment']['data']

      lookml = json.loads(data)[0]['info_scheming.lookml'];

      g = git.cmd.Git(git_dir)
      g.pull()

      f = open(git_dir+'/'+filename, 'w')
      f.write(lookml)
      f.close()
      g.add(filename)
      g.commit('-m', 'commit')
      g.push()

      return '', 200

    else:
        abort(400)

@app.route('/info_in_rows', methods=['POST'])
def info_in_rows():
    if request.method == 'POST':
      print(request.json)
      payload = request.json

      data = json.loads(payload['attachment']['data'])

      vw = View(str(data[0]['info_in_rows.view_name_lookml']))
      vw.setSqlTableName(sql_table_name=str(data[0]['info_in_rows.table_name']),schema=str(data[0]['info_in_rows.table_schema']))
      vw.setFolder(git_dir)

      for row in data:
        column = str(row['info_in_rows.column_name'])
        
        if str(row['info_in_rows.type_convert']) == 'time':
          dim = DimensionGroup(dbColumn=column)
        else:
          dim = Dimension(dbColumn=column)
          dim.setType(str(row['info_in_rows.type_convert']))

        if row['info_in_rows.comment'] is not None:
          dim.setProperty('description', str(row['info_in_rows.comment']))

        vw + dim

      g = git.cmd.Git(git_dir)
      g.pull()
      vw.path = git_dir + '/' + vw.fileName # REMOVE WHEN write is updated
      vw.write()
      g.add(vw.fileName)
      g.commit('-m', '"new commit"')
      g.push()

      return '', 200

    else:
        abort(400)


if __name__ == '__main__':
    app.run(host="127.0.0.1", threaded=True, debug=True)
