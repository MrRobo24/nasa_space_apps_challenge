import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;

public class Receiving extends Thread{

	public void run()
	{
		Socket s;
		ServerSocket ss;
		InputStreamReader isr;
		BufferedReader br;
		String message;
	
		try
		{
			while(true)
			{
				ss = new ServerSocket(8000);
				s=ss.accept();
				System.out.println("CONNECTION MADE:\n");
				isr=new InputStreamReader(s.getInputStream());
				br=new BufferedReader(isr);
				message=br.readLine();
				
			
			if(message.equals(""))
				System.out.println("Android Empty:"+message);
			else
			{
				System.out.println(message);
				new SendingToPython(message).start();
				s.close();
				ss.close();
			}
			}
			
		}
		
		catch(IOException e)
		{
			e.printStackTrace();
		}
	}
}
