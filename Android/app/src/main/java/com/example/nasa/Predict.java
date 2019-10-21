package com.example.nasa;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.Manifest;
import android.content.Context;
import android.content.pm.PackageManager;
import android.graphics.Color;
import android.location.Address;
import android.location.Geocoder;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.view.View;
import android.widget.Button;
import android.widget.SeekBar;
import android.widget.Toast;

import com.razerdp.widget.animatedpieview.AnimatedPieView;
import com.razerdp.widget.animatedpieview.AnimatedPieViewConfig;
import com.razerdp.widget.animatedpieview.callback.OnPieSelectListener;
import com.razerdp.widget.animatedpieview.data.IPieInfo;
import com.razerdp.widget.animatedpieview.data.SimplePieInfo;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.List;
import java.util.Locale;

public class Predict extends AppCompatActivity implements LocationListener  {

    //Button clickable;
    public String message="0";
    public  String latlong, flag;
    LocationManager locationManager;
    SeekBar seekBar;
    int progseek;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_predict);

        //clickable = (Button) findViewById(R.id.check_safety);

        if (ContextCompat.checkSelfPermission(getApplicationContext(), Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(getApplicationContext(), Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {

            ActivityCompat.requestPermissions(this, new String[]{Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION}, 101);

        }





        getLocation();
        MessageSender messageSender = new MessageSender();
        messageSender.execute(latlong);
        Toast.makeText(getApplicationContext(),"Sent location",Toast.LENGTH_SHORT).show();

        Thread myThread = new Thread(new MyServerThread());
        myThread.start();

        //MyServerThread o=new MyServerThread();




       /* clickable.setOnClickListener(new View.OnClickListener() {
            public void onClick(View v) {
                Predict.MessageSender messageSender = new Predict.MessageSender();

                //latlong=a+" "+b;
                Toast.makeText(getApplicationContext(),"Sent location",Toast.LENGTH_SHORT).show();
                messageSender.execute(latlong);
            }
        });*/





    }

    void getLocation() {
        try {
            locationManager = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
            locationManager.requestLocationUpdates(LocationManager.NETWORK_PROVIDER, 5000, 5, this);
        } catch (SecurityException e) {
            e.printStackTrace();
        }
    }


    @Override
    public void onLocationChanged(final Location location) {
        latlong = location.getLatitude() + " " + location.getLongitude();
        //locationText.setText("Latitude: " + location.getLatitude() + "\n Longitude: " + location.getLongitude());

       /* try {
            Geocoder geocoder = new Geocoder(this, Locale.getDefault());
            List<Address> addresses = geocoder.getFromLocation(location.getLatitude(), location.getLongitude(), 1);
            //locationText.setText(locationText.getText() + "\n"+addresses.get(0).getAddressLine(0)+", "+
                    addresses.get(0).getAddressLine(1)+", "+addresses.get(0).getAddressLine(2));
        }catch(Exception e)
        {

        }*/

    }

    @Override
    public void onProviderDisabled(String provider) {
        Toast.makeText(Predict.this, "Please Enable GPS and Internet", Toast.LENGTH_SHORT).show();
    }

    @Override
    public void onStatusChanged(String provider, int status, Bundle extras) {

    }

    @Override
    public void onProviderEnabled(String provider) {

    }


    class MessageSender extends AsyncTask<String,Void,Void> {

        Socket s;
        DataOutputStream dos;
        BufferedWriter pw;

        protected Void doInBackground(String... voids)
        {
            flag="2";
            message="23.4 72.3 "+flag;

            try
            {
                s=new Socket("192.168.43.22",9090);
                pw=new BufferedWriter(new OutputStreamWriter(s.getOutputStream()));
                pw.write(message+"\n",0,message.length());
                pw.newLine();
                pw.flush();
                pw.close();
            }
            catch(IOException e)
            {
                e.printStackTrace();
            }
            return  null;
        }

    }

    public class MyServerThread implements Runnable
    {
        public String message;
        Socket s;
        ServerSocket ss;
        InputStreamReader isr;
        BufferedReader br;
        Handler h = new Handler();
       // String message="55";

        @Override
        public void run()
        {


            try
            {
                ss = new ServerSocket(8080);            //8080 original
                while(true)
                {
                    s=ss.accept();
                    isr =new InputStreamReader(s.getInputStream());
                    br = new BufferedReader(isr);
                    message = br.readLine();
                    final String details[]=message.split(" ");
                    //message="55";
                    h.post(new Runnable()
                    {
                        public void run() {
                            Toast.makeText(getApplicationContext(), message, Toast.LENGTH_SHORT).show();
                            //int t=Integer.parseInt(message);
                            //String temp="Fire Probability="+t+" ";

                            AnimatedPieView animatedPieView=findViewById(R.id.pieView);
                            AnimatedPieViewConfig config=new AnimatedPieViewConfig();
                            config.addData(new SimplePieInfo(Double.parseDouble(message), Color.parseColor("#FF0000"),"Danger Meter"));
                            config.addData(new SimplePieInfo(100-Double.parseDouble(message), Color.parseColor("#AAFF00"),"Safe Meter"));
                            config.duration(1000);
                            config.drawText(true);
                            config.strokeMode(true);
                            config.textSize(52);
                            config.selectListener(new OnPieSelectListener<IPieInfo>() {
                                @Override
                                public void onSelectPie(@NonNull IPieInfo pieInfo, boolean isFloatUp) {
                                    Toast.makeText(Predict.this,pieInfo.getDesc()+" - "+pieInfo.getValue(),Toast.LENGTH_SHORT).show();
                                }
                            });
                            config.startAngle(-180);
                            animatedPieView.applyConfig(config);
                            animatedPieView.start();




                            //  if(details[2]<=3.00)

                        }
                    });
                }

            }catch(Exception e) {

                Toast.makeText(getApplicationContext(), "Fail", Toast.LENGTH_SHORT).show();
                e.printStackTrace();
            }

        }

    }
}
