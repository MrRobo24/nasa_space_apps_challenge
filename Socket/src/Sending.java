import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;

public class Sending extends Thread {
	String message;
	
	public Sending(String message) {
		super();
		this.message = message;
	}

	public void run()
	{
		try
		{
			Socket s1=new Socket("192.168.0.101",8080);
			PrintWriter pw=new PrintWriter(s1.getOutputStream());
			pw.write(message);
			pw.flush();
			pw.close();
			s1.close();
	}
	catch(IOException e)
	{
		e.printStackTrace();
	}
	}
	
}

