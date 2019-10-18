package com.example.testmap;

import android.os.Bundle;
import android.util.Log;

import androidx.fragment.app.FragmentActivity;

import com.google.android.gms.maps.CameraUpdateFactory;
import com.google.android.gms.maps.GoogleMap;
import com.google.android.gms.maps.OnMapReadyCallback;
import com.google.android.gms.maps.SupportMapFragment;
import com.google.android.gms.maps.model.LatLng;
import com.google.android.gms.maps.model.MarkerOptions;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.Charset;
import java.util.ArrayList;
import java.util.List;



//package com.example.testmap;

class Coordinates
{
    private String slno;
    private double latitude;
    private double longitude;

    public String getSlno() {
        return slno;
    }

    public void setSlno(String slno) {
        this.slno = slno;
    }

    public double getLatitude() {
        return latitude;
    }

    public void setLatitude(double latitude) {
        this.latitude = latitude;
    }

    public double getLongitude() {
        return longitude;
    }

    public void setLongitude(double longitude) {
        this.longitude = longitude;
    }
}



public class MapsActivity extends FragmentActivity implements OnMapReadyCallback
{

    private GoogleMap mMap;

    @Override
    protected void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_maps);
        // Obtain the SupportMapFragment and get notified when the map is ready to be used.
        SupportMapFragment mapFragment = (SupportMapFragment) getSupportFragmentManager().findFragmentById(R.id.map);
        mapFragment.getMapAsync(this);
    }


    /**
     * Manipulates the map once available.
     * This callback is triggered when the map is ready to be used.
     * This is where we can add markers or lines, add listeners or move the camera. In this case,
     * we just add a marker near Sydney, Australia.
     * If Google Play services is not installed on the device, the user will be prompted to install
     * it inside the SupportMapFragment. This method will only be triggered once the user has
     * installed Google Play services and returned to the app.
     */
    @Override
    public void onMapReady(GoogleMap googleMap)
    {
        mMap = googleMap;
        /*String ll[]={"8.1525 93.4988" ,
                "8.1488 93.4908" ,
                "8.1512 93.4984" ,
                "8.1559 93.4903" ,
                "8.1576 93.5015" ,
                "8.177 93.5052" ,
                "8.1855 93.5061" ,
                "8.186 93.5039" ,
                "8.1881 93.4915" ,
                "8.1888 93.4937" ,
                "8.1899 93.4917"};

        int len=ll.length;
        int i;

        for(i=0;i<len;i++)
        {
            String x[]=ll[i].split(" ");
            LatLng location=new LatLng(Double.parseDouble(x[0]), Double.parseDouble(x[1]));
            mMap.addMarker(new MarkerOptions().position(location).title("Marker in fire"));//.icon(BitmapDescriptorFactory.fromResource(R.drawable.marker1)));
            mMap.moveCamera(CameraUpdateFactory.newLatLng(location));
        }*/

        List<Coordinates> coordinates=new ArrayList<>();
        InputStream is=getResources().openRawResource(R.raw.area);
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
                sample.setSlno(tokens[0]);
                sample.setLatitude(Double.parseDouble(tokens[1]));
                sample.setLongitude(Double.parseDouble(tokens[2]));
                coordinates.add(sample);
                LatLng location=new LatLng(sample.getLatitude(), sample.getLongitude());
                mMap.addMarker(new MarkerOptions().position(location).title("Marker in "+sample.getSlno()));//.icon(BitmapDescriptorFactory.fromResource(R.drawable.marker1)));
                mMap.moveCamera(CameraUpdateFactory.newLatLng(location));
                Log.d("MapsActivity","Just Created:"+sample);
            }
        }
        catch(IOException e)
        {
            Log.v("MapsActivity","Error reading data file on line "+line,e);
            e.printStackTrace();
        }
    }
}