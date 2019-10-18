import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;

class Client extends Thread
{
  private Socket socket = null;
  private static BufferedReader reader = null;
  private static BufferedWriter writer = null;
  private static ServerSocket ss =  null;
  private static Socket s = null;

  public Client()
  {
	  
  }
  public Client(InetAddress address, int port) throws IOException
  {
     socket = new Socket(address, port);
     reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
     writer = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
  }

  public void send(String msg) throws IOException
  {
     writer.write(msg, 0, msg.length());
     writer.newLine();
     writer.flush();
  }
  public void sen(String msg) throws IOException
  {
	  writer = new BufferedWriter(new OutputStreamWriter(s.getOutputStream()));
     writer.write(msg, 0, msg.length());
     writer.newLine();
     writer.flush();
  }

  public String recv() throws IOException
  {
	  
	  
  String ans = "";
  System.out.println("ENTERED\n");
	 while(true)
	 {
	 ans = reader.readLine();
	 if(!ans.equals(""))
	 break;
	 }
 
     return ans;
  }
  public String rec() throws IOException
  {
	 // ss = new ServerSocket(8000);
	 // s=ss.accept();
	  
	  
  String ans = "";
  System.out.println("ENTERED\n");
	 while(true)
	 {
		 reader = new BufferedReader(new InputStreamReader(s.getInputStream()));
	 ans = reader.readLine();
	 if(!ans.equals(""))
	 break;
	 }
 
     return ans;
  }

  public static void main(String[] args)
  {
  try {
	  
	   Client android = new Client();
	   android.ss =new ServerSocket(8000);
	   android.s = ss.accept();

       InetAddress host1 = InetAddress.getByName("192.168.0.101");
       //Client client1 = new Client(host1, 8000);
       //String response1 = client1.recv();
       String response1 = android.rec();
       response1="28.8647 79.8665";
       System.out.println("Client1 received: " + response1);
       
       InetAddress host2 = InetAddress.getByName("192.168.0.110");
       Client client2 = new Client(host2, 9000);
//String response1 = "0 0";
       client2.send(response1);
       System.out.println("Data sent to client2");
       String response2 = client2.recv();
       System.out.println("Client2 received: " + response2);
       
       
       //android.socket = Client.s;
       
       android.sen(response2);
       System.out.println("SENT");
       
    }
    catch (IOException e) {
       System.out.println("Caught Exception: " + e.toString());
    }
     
     
     
  }
}