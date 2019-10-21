package com.example.nasa;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;
import androidx.fragment.app.Fragment;
import androidx.fragment.app.FragmentActivity;

import android.Manifest;
import android.content.pm.PackageManager;
import android.location.Location;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Handler;
import android.util.Log;
import android.view.View;
import android.widget.Toast;

import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationServices;
import com.google.android.gms.maps.CameraUpdate;
import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.BitmapDescriptorFactory;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.android.gms.tasks.Task;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.nio.charset.Charset;

public class NasaData extends FragmentActivity implements OnMapReadyCallback {

    Location currentLocation;
    FusedLocationProviderClient fusedLocationProviderClient;
    private static final int REQUEST_CODE=101;
    public String latlong,flag,a,b;
    public String details[],readmsg[];

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_nasa_data);

        fusedLocationProviderClient= LocationServices.getFusedLocationProviderClient(this);
        fetchLastLocation();

      //  Thread myThread = new Thread(new NasaData.MyServerThread());
       // myThread.start();
    }

    private void fetchLastLocation() {
        if(ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION)!=PackageManager.PERMISSION_GRANTED)
        {
            ActivityCompat.requestPermissions(this,new String[]{
                    Manifest.permission.ACCESS_FINE_LOCATION},REQUEST_CODE);
            return;

        }

        Task<Location> task=fusedLocationProviderClient.getLastLocation();
        task.addOnSuccessListener(new OnSuccessListener<Location>() {
            @Override
            public void onSuccess(Location location) {
                if(location!=null)
                {
                    currentLocation=location;
                    latlong=currentLocation.getLatitude()+" "+currentLocation.getLongitude();
                   // NasaData.MessageSender messageSender = new NasaData.MessageSender();
                    //messageSender.execute(currentLocation.getLatitude()+" "+currentLocation.getLongitude());

                  //  Toast.makeText(getApplicationContext(),latlong,Toast.LENGTH_SHORT).show();

                    SupportMapFragment supportMapFragment=(SupportMapFragment)
                            getSupportFragmentManager().findFragmentById(R.id.google_map);
                    supportMapFragment.getMapAsync(NasaData.this);
                }
            }
        });
    }



    //@Override
    public void onRequestPermissionResult(int requestCode, @NonNull String[] permissions,@NonNull int[] grantResults)
    {
        switch (requestCode)
        {
            case REQUEST_CODE:
                if (grantResults.length>0&&grantResults[0]==PackageManager.PERMISSION_GRANTED){
                    fetchLastLocation();
                }
                break;
        }
    }

    @Override
    public void onMapReady(GoogleMap googleMap) {
        Check_Safety o=new Check_Safety();
        String details[]=(o.tmpmsg).split(" ");

        /*

        for(i=0;i<len;i++)
        {
            String x[]=ll[i].split(" ");
            LatLng location=new LatLng(Double.parseDouble(x[0]), Double.parseDouble(x[1]));
            mMap.addMarker(new MarkerOptions().position(location).title("Marker in fire"));//.icon(BitmapDescriptorFactory.fromResource(R.drawable.marker1)));
            mMap.moveCamera(CameraUpdateFactory.newLatLng(location));
        }*/

        // List<Coordinates> coordinates=new ArrayList<>();
        InputStream is=getResources().openRawResource(R.raw.currentzone);
        BufferedReader br=new BufferedReader(new InputStreamReader(is, Charset.forName("UTF-8")));

        String line="";
        try
        {
            br.readLine();
            while((line=br.readLine())!=null)
            {
                Log.d("MapsActivity","Line:"+line);
                String[] tokens=line.split(",");

                Coordinates sample=new Coordinates();
                sample.setLatitude(Double.parseDouble(tokens[0]));
                sample.setLongitude(Double.parseDouble(tokens[1]));
                // coordinates.add(sample);

                LatLng location=new LatLng(sample.getLatitude(), sample.getLongitude());
                googleMap.addMarker(new MarkerOptions().position(location).icon(BitmapDescriptorFactory.fromResource(R.drawable.mark)));//.icon(BitmapDescriptorFactory.fromResource(R.drawable.marker1)))

                googleMap.moveCamera(CameraUpdateFactory.newLatLng(location));
                Log.d("MapsActivity","Just Created:"+sample);
            }
        }
        catch(IOException e)
        {
            Log.v("MapsActivity","Error reading data file on line "+line,e);
            e.printStackTrace();
        }



        /*for(int i=2;i<details.length;i++)
        {
            String readmsg[]=details[i].split(",");
            LatLng loc=new LatLng(Double.parseDouble(readmsg[0]),Double.parseDouble(readmsg[1]));
            MarkerOptions markerOptions=new MarkerOptions().position(loc);
            googleMap.addMarker(markerOptions);
        }*/


    }


  /*  class MyServerThread implements Runnable
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
                    details=message.split(" ");



                    h.post(new Runnable()
                    {
                        public void run() {
                            Toast.makeText(getApplicationContext(), "Marked", Toast.LENGTH_SHORT).show();



                        }
                    });
                    ss.close();
                    s.close();
                }

            }catch(IOException e)
            {
                // Toast.makeText(getApplicationContext(), message, Toast.LENGTH_SHORT).show();
                e.printStackTrace();
            }
        }



    }*/



}


