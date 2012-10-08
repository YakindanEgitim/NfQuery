# This file is part of NfQuery.  NfQuery is free software: you can
# redistribute it and/or modify it under the terms of the GNU General Public
# License as published by the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright NfQuery Team Members

<link rel="stylesheet" href="/nfsen/plugins/nfquery/css/bootstrap.css" />

<?php

/*
 * Frontend plugin: demoplugin
 *
 * Required functions: demoplugin_ParseInput and demoplugin_Run
 *
 */

/* 
 * demoplugin_ParseInput is called prior to any output to the web browser 
 * and is intended for the plugin to parse possible form data. This 
 * function is called only, if this plugin is selected in the plugins tab. 
 * If required, this function may set any number of messages as a result 
 * of the argument parsing.
 * The return value is ignored.
 */

include('/var/www/nfsen/details.php');

function nfquery_ParseInput( $plugin_id ) {
	Process_Details_tab(0, 0);
	#SetMessage('error', "Error set by demo plugin!");
	#SetMessage('warning', "Warning set by demo plugin!");
	#SetMessage('alert', "Alert set by demo plugin!");
    #SetMessage('info', "Info set by demo plugin!");

} // End of demoplugin_ParseInput


/*
 * This function is called after the header and the navigation bar have 
 * are sent to the browser. It's now up to this function what to display.
 * This function is called only, if this plugin is selected in the plugins tab
 * Its return value is ignored.
 */
function nfquery_Run( $plugin_id ) {
	    require_once('nfquery/nfqueryutil.php');

		#print '<iframe id="nfqueryIFrame" src="/nfsen/plugins/nfquery/index.php" frameborder="0" style="height:100%;width:100%" scrolling="no">IFrame</iframe>';
		if(isset($_POST['nfqueryTabName'])){
				
			if(!isset($_SESSION['nfquery'])){	
				$_SESSION['nfquery'] = array();
			}
			$_SESSION['nfquery']['nfqueryTabName'] = $_POST['nfqueryTabName'];
		}
		if(!isset($_SESSION['nfquery']['nfqueryTabName']))
			$_SESSION['nfquery']['nfqueryTabName'] = "Settings";
			
		include("nfquery/index.php");
	
##		if(file_exists("/home/ahmetcan/nfquery/plugin/backend/nfquery.plugin.conf")){
##			$result  = isRegister();
##			if($result==0){
##				echo "<div class='alert alert-error span11'> Your plugin is not registered to QueryServer yet.</div>";
##
##			}
##			if($result==1){
##			         include('nfquery/index.php');
##			}
##		}
##		else{
##			include('nfquery/conf.php');
##		}
#		if(file_exists("/tmp/nfquery.plugin.conf")){
#			$result  = isRegistered();
#			// 0:plugin has not    1:reject plugin    2:request pending     3:plugin registered
#			if($result == 0){
#				include('nfquery/conf.php');
#			}
#			else if($result==1){
#				include('nfquery/settings.php');
#			}
#			else if($result==2){
#				include('nfquery/settings.php');
#			}
#			else if($result==3){
#				include('nfquery/settings.php');
#			}
#	#		echo "<div class='alert alert-info span11'><img src='/nfsen/plugins/nfquery/img/button_ok.png'>Your Plugin Informations has been Saved</div>";
#			
#		#	include('nfquery/index.php');
#		}
#		else{
#			include('nfquery/conf.php');
#		}
} // End of demoplugin_Run


?>
