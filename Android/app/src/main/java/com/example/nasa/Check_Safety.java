        package com.example.nasa;

        import android.Manifest;
        import android.annotation.SuppressLint;
        import android.content.Intent;
        import android.content.pm.PackageManager;
        import android.location.Location;
        import android.location.LocationListener;
        import android.location.LocationManager;
        import android.os.Build;
        import android.os.Bundle;
        import android.os.Handler;
        import android.provider.Settings;
        import android.view.View;
        import android.widget.Button;
        import android.widget.TextView;

        import androidx.annotation.NonNull;
        import androidx.annotation.Nullable;
        import androidx.appcompat.app.AppCompatActivity;
        import androidx.core.app.ActivityCompat;

        import android.content.Context;
        import android.content.pm.PackageManager;
        import android.location.Address;
        import android.location.Geocoder;
        import android.location.Location;
        import android.location.LocationListener;
        import android.location.LocationManager;
        import android.os.Bundle;
        import android.view.View;
        import android.widget.Button;
        import android.widget.TextView;
        import android.widget.Toast;

        import androidx.appcompat.app.AppCompatActivity;
        import androidx.core.app.ActivityCompat;
        import androidx.core.content.ContextCompat;

        import java.io.BufferedReader;
        import java.io.BufferedWriter;
        import java.io.DataOutputStream;
        import java.io.InputStreamReader;
        import java.io.OutputStreamWriter;
        import java.net.ServerSocket;
        import java.util.List;
        import java.util.Locale;
        import android.os.AsyncTask;
        import android.os.Bundle;
        import android.view.View;
        import android.widget.Button;
        import android.widget.EditText;
        import android.widget.Toast;


        import androidx.appcompat.app.AppCompatActivity;

        import java.io.IOException;
        import java.io.PrintWriter;
        import java.net.Socket;
        import java.net.UnknownHostException;

        public class Check_Safety extends AppCompatActivity implements LocationListener {

            Button getLocationBtn,clickable;
            TextView locationText,textbox;
            String latlong,mssg;
            Location l;
            LocationManager locationManager;

            @Override
            protected void onCreate(Bundle savedInstanceState) {
                super.onCreate(savedInstanceState);
                getSupportActionBar().hide();
                setContentView(R.layout.activity_check__safety);

                //getLocationBtn = (Button)findViewById(R.id.getLocationBtn);
                locationText = (TextView)findViewById(R.id.locationText);
                clickable = (Button)findViewById(R.id.sendLocationBtn);
                textbox=(TextView)findViewById(R.id.Textbox);


                Thread myThread = new Thread(new MyServerThread());
                myThread.start();

                if (ContextCompat.checkSelfPermission(getApplicationContext(), android.Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(getApplicationContext(), android.Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {

                    ActivityCompat.requestPermissions(this, new String[]{android.Manifest.permission.ACCESS_FINE_LOCATION, android.Manifest.permission.ACCESS_COARSE_LOCATION}, 101);

                }


                getLocation();



                clickable.setOnClickListener(new View.OnClickListener(){
                    public void onClick(View v){
                        double a=l.getLatitude();
                        double b=l.getLongitude();
                        MessageSender messageSender = new MessageSender();
                        latlong=a+" "+b;
                        messageSender.execute(latlong);
                    }
                });
            }

            void getLocation() {
                try {
                    locationManager = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
                    locationManager.requestLocationUpdates(LocationManager.NETWORK_PROVIDER, 5000, 5, this);
                }
                catch(SecurityException e) {
                    e.printStackTrace();
                }
            }




            @Override
            public void onLocationChanged(final Location location) {
                l=location;
                locationText.setText("Latitude: " + location.getLatitude() + "\n Longitude: " + location.getLongitude());

                try {
                    Geocoder geocoder = new Geocoder(this, Locale.getDefault());
                    List<Address> addresses = geocoder.getFromLocation(location.getLatitude(), location.getLongitude(), 1);
                    locationText.setText(locationText.getText() + "\n"+addresses.get(0).getAddressLine(0)+", "+
                            addresses.get(0).getAddressLine(1)+", "+addresses.get(0).getAddressLine(2));
                }catch(Exception e)
                {

                }

            }

            @Override
            public void onProviderDisabled(String provider) {
                Toast.makeText(Check_Safety.this, "Please Enable GPS and Internet", Toast.LENGTH_SHORT).show();
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
                    String message=voids[0];

                    try
                    {
                        s=new Socket("192.168.0.122",8000);
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

            class MyServerThread implements Runnable
            {
                Socket s;
                ServerSocket ss;
                InputStreamReader isr;
                BufferedReader br;
                Handler h = new Handler();
                String message="Test";
                @Override
                public void run()
                {
                    try
                    {
                        ss = new ServerSocket(8080);
                        while(true)
                        {
                            s=ss.accept();
                            isr =new InputStreamReader(s.getInputStream());
                            br = new BufferedReader(isr);
                            message = br.readLine();

                            h.post(new Runnable()
                            {
                                public void run() {
                                    Toast.makeText(getApplicationContext(), message, Toast.LENGTH_SHORT).show();
                                }
                            });
                        }
                    }catch(IOException e)
                    {
                        Toast.makeText(getApplicationContext(), message, Toast.LENGTH_SHORT).show();
                        e.printStackTrace();
                    }
                }

            }




        }
