 @app.route("/reports_map")
 @login_required
 def reports_map():
     reports = Report.query.all()
     reports_data = [
         {
             "id": report.id,
             "user_id": report.user_id,
             "description": report.description,
             "latitude": report.latitude,
             "longitude": report.longitude,
             "timestamp": report.timestamp.isoformat(),
             "damage_type": report.damage_type
         } 
         for report in reports
     ]
     return render_template('reports_map.html', reports=reports_data)