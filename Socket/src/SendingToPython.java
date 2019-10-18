import java.io.BufferedWriter;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.net.InetAddress;
//import java.io.PrintWriter;
//import java.io.Writer;
import java.net.Socket;


public class SendingToPython extends Thread{
	private Socket socket = null;
	  private BufferedWriter writer = null;
	String message;
	
	
	public SendingToPython(String message) {
		super();
		this.message = message;
	} 
	
	public SendingToPython(String string, int port) throws IOException
	{
		socket=new Socket(string,port);
	}
	public void send(String msg) throws IOException
	  {
	     writer.write(msg, 0, msg.length());
	     writer.newLine();
	     writer.flush();
	  }

	public void run()
	{
		try
		{
			SendingToPython obj = new SendingToPython("192.168.0.122",9000);
			obj.send(message);
			System.out.println("CONNECTION MADE:\n");
			BufferedWriter pw=new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
			pw.write(message+"\n",0,message.length());
			pw.newLine();
			System.out.println(message);
			pw.flush();
			pw.close();
			socket.close();
		}
		catch(IOException e)
		{
			e.printStackTrace();
		}
	}
}
