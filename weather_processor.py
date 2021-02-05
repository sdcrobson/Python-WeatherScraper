
import wx
import locale
import logging
from db_operations import DBOperations
from scrape_weather import WeatherScraper
from plot_operations import PlotOperations

logging.basicConfig(format='%(levelname)s:%(message)s %(asctime)s', 
                    filename="weatherScraper.log", 
                    level=logging.DEBUG,filemode = "w", 
                    datefmt='%m/%d/%Y %I:%M:%S %p'
                    )

class MyFrame1(wx.Frame):

    
	
	def __init__( self, parent ):
		
		locale.setlocale(locale.LC_ALL, 'en_US')
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString ) )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_APPWORKSPACE ) )
		
		bSizer25 = wx.BoxSizer( wx.VERTICAL )
		
		bSizer26 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText32 = wx.StaticText( self, wx.ID_ANY, u"Weather Data", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText32.Wrap( -1 )
		self.m_staticText32.SetFont( wx.Font( 20, 72, 90, 90, False, "Headline R" ) )
		
		bSizer26.Add( self.m_staticText32, 0, wx.ALL, 5 )
		
		
		bSizer25.Add( bSizer26, 1, wx.EXPAND, 5 )
		
		bSizer28 = wx.BoxSizer( wx.HORIZONTAL )
		
		sbSizer4 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Boxplot" ), wx.HORIZONTAL )
		
		self.lblStarYear = wx.StaticText( sbSizer4.GetStaticBox(), wx.ID_ANY, u"Start Year:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblStarYear.Wrap( -1 )
		self.lblStarYear.SetFont( wx.Font( 9, 74, 90, 90, False, "Britannic Bold" ) )
		
		sbSizer4.Add( self.lblStarYear, 1, wx.ALL, 5 )
		
		self.txtYearOne = wx.TextCtrl( sbSizer4.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer4.Add( self.txtYearOne, 1, wx.ALL, 5 )
		
		self.lblEndYear = wx.StaticText( sbSizer4.GetStaticBox(), wx.ID_ANY, u"End Year:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblEndYear.Wrap( -1 )
		self.lblEndYear.SetFont( wx.Font( 9, 74, 90, 90, False, "Britannic Bold" ) )
		
		sbSizer4.Add( self.lblEndYear, 1, wx.ALL, 5 )
		
		self.txtYearTwo = wx.TextCtrl( sbSizer4.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer4.Add( self.txtYearTwo, 1, wx.ALL, 5 )
		
		self.btnBoxPlot = wx.Button( sbSizer4.GetStaticBox(), wx.ID_ANY, u"Generate", wx.DefaultPosition, wx.Size( -1,30 ), 0 )
		self.btnBoxPlot.SetFont( wx.Font( 9, 74, 90, 90, False, "Britannic Bold" ) )
		self.btnBoxPlot.Bind(wx.EVT_BUTTON, self.OnClickedBoxPlot)
		
		sbSizer4.Add( self.btnBoxPlot, 0, wx.ALL, 5 )
		
		
		bSizer28.Add( sbSizer4, 1, wx.EXPAND, 5 )
		
		
		bSizer25.Add( bSizer28, 1, wx.EXPAND, 5 )
		
		bSizer29 = wx.BoxSizer( wx.HORIZONTAL )
		
		sbSizer5 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Linegraph" ), wx.HORIZONTAL )
		
		self.lblYear = wx.StaticText( sbSizer5.GetStaticBox(), wx.ID_ANY, u"Year:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblYear.Wrap( -1 )
		self.lblYear.SetFont( wx.Font( 9, 74, 90, 90, False, "Britannic Bold" ) )
		
		sbSizer5.Add( self.lblYear, 1, wx.ALL, 5 )
		
		self.txtYear = wx.TextCtrl( sbSizer5.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer5.Add( self.txtYear, 1, wx.ALL, 5 )
		
		self.lblMonth = wx.StaticText( sbSizer5.GetStaticBox(), wx.ID_ANY, u"Month:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.lblMonth.Wrap( -1 )
		self.lblMonth.SetFont( wx.Font( 9, 74, 90, 90, False, "Britannic Bold" ) )
		
		sbSizer5.Add( self.lblMonth, 1, wx.ALL, 5 )
		
		self.txtMonth = wx.TextCtrl( sbSizer5.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		sbSizer5.Add( self.txtMonth, 1, wx.ALL, 5 )
		
		self.btnLineGraph = wx.Button( sbSizer5.GetStaticBox(), wx.ID_ANY, u"Generate", wx.DefaultPosition, wx.Size( -1,30 ), 0 )
		self.btnLineGraph.SetFont( wx.Font( 9, 74, 90, 90, False, "Britannic Bold" ) )
		self.btnLineGraph.Bind(wx.EVT_BUTTON, self.OnClickedLineGraph)

		
		sbSizer5.Add( self.btnLineGraph, 1, wx.ALL, 5 )
		
		
		bSizer29.Add( sbSizer5, 1, wx.EXPAND, 5 )
		
		
		bSizer25.Add( bSizer29, 1, wx.EXPAND, 5 )
		
		bSizer30 = wx.BoxSizer( wx.HORIZONTAL )
		
		sbSizer6 = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"Manage Weather Data" ), wx.HORIZONTAL )
		
		self.btnDownload = wx.Button( sbSizer6.GetStaticBox(), wx.ID_ANY, u"Download", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btnDownload.SetFont( wx.Font( 9, 74, 90, 90, False, "Britannic Bold" ) )
		self.btnDownload.Bind(wx.EVT_BUTTON, self.OnClickedDownload)


		
		sbSizer6.Add( self.btnDownload, 1, wx.ALL, 5 )
		
		self.btnUpdate = wx.Button( sbSizer6.GetStaticBox(), wx.ID_ANY, u"Update", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.btnUpdate.SetFont( wx.Font( 9, 74, 90, 90, False, "Britannic Bold" ) )
		self.btnUpdate.Bind(wx.EVT_BUTTON, self.OnClickedUpdate)


		
		sbSizer6.Add( self.btnUpdate, 1, wx.ALL, 5 )
		
		
		bSizer30.Add( sbSizer6, 1, wx.EXPAND, 5 )
		
		
		bSizer25.Add( bSizer30, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer25 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def OnClickedBoxPlot(self, event):
		plot = PlotOperations()
		plot.boxplot(self.txtYearOne.GetValue(), self.txtYearTwo.GetValue())
		

	def OnClickedLineGraph(self,event):
		plot = PlotOperations()
		plot.linegraph(self.txtYear.GetValue(), self.txtMonth.GetValue())

	def OnClickedDownload(self, event):	
		db = DBOperations()
		db.purge_data()
		db.initialize_db()
		scraper = WeatherScraper()
		scraper.start_scraping()

	def OnClickedUpdate(self, event):
		scraper = WeatherScraper()
		scraper.start_scraping()
		
	def __del__( self ):
		pass

class WeatherProcessor(wx.App):
    def OnInit(self):
        mainFrame = MyFrame1(None)

        mainFrame.Show(True)
        
        
        return True

if __name__ == "__main__":
	app = WeatherProcessor()
	app.MainLoop()
		