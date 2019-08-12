package com.example.pzhang222.helloworld;

import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.app.Activity;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.TextView;

import java.lang.reflect.Field;
import java.util.HashSet;
import java.util.Random;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Vector;
import java.util.ArrayList;

public class Colors extends Activity {

    private static LinkedHashSet<Integer> colorSet_ = new LinkedHashSet<Integer>();
    private static List<String> colorNames_ = new Vector<String>();
    private static int answer_;
    private static int a_;
    private static int b_;
    private static int c_;

    @Override
    protected void onCreate(Bundle savedInstanceState) 
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings);

        TextView view = (TextView) findViewById(R.id.guessView);
        view.setText("Color");
        view.setTextColor(Color.RED);

        colorNames_.add("blue");
        colorNames_.add("black");
        colorNames_.add("red");

        colorNames_.add("green");
        colorNames_.add("yellow");
        colorNames_.add("white");
        colorNames_.add("gray");
        colorNames_.add("brown");
        colorNames_.add("purple");
        colorNames_.add("orange");
        colorNames_.add("cyan");
        colorNames_.add("magenta");

        updateGame();
    }

    private int translateColor(String colorString)
    {
        if (colorString == "purple")
            return Color.parseColor("#4B0082");
        else if (colorString == "orange")
            return Color.parseColor("#FFA500");
        else if (colorString == "brown")
            return Color.parseColor("#8B4513");

        return Color.parseColor(colorString);
    }

    private void updateGame() 
    {
        colorSet_.clear();
        do 
        {
            int index = new Random().nextInt(colorNames_.size());
            colorSet_.add(index);
        } 
        while (colorSet_.size() <= 2);

        int tmode = new Random().nextInt(3);
        TextView mode = (TextView) findViewById(R.id.mode);

        List<Integer> list = new ArrayList<Integer>(colorSet_);

        int firsti = list.get(0);
        String firstcolor = colorNames_.get(firsti);

        int secondi = list.get(1);
        String secondcolor = colorNames_.get(secondi);

        int threei = list.get(2);
        String thirdcolor = colorNames_.get(threei);

        if (tmode == 0)
        {
            mode.setText("background color");
        }
        else if (tmode == 1)
        {
            mode.setText("text color");
        }
        else if (tmode == 2)
        {
            mode.setText("word");
        }

        answer_ = tmode;

        TextView view = (TextView) findViewById(R.id.guessView);

        Log.d("answer_= ",Integer.toString(answer_));
        getWindow().getDecorView().setBackgroundColor(translateColor(firstcolor));
        view.setTextColor(translateColor(secondcolor));
        view.setText(thirdcolor);

        if (firsti <= 2)
            mode.setTextColor(Color.WHITE);
        else
            mode.setTextColor(Color.BLACK);

        Button one = (Button) findViewById(R.id.button1);
        one.setOnClickListener(listenOne);
        one.setText(firstcolor);

        Button two = (Button) findViewById(R.id.button2);
        two.setOnClickListener(listenTwo);
        two.setText(secondcolor);

        Button three = (Button) findViewById(R.id.button3);
        three.setOnClickListener(listenThree);
        three.setText(thirdcolor);
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu)
    {
        MenuItem menuItem = menu.add(Menu.NONE, 1, Menu.NONE, R.string.title_about);
        menuItem.setShowAsAction(MenuItem.SHOW_AS_ACTION_IF_ROOM);
        menuItem.setIcon(R.drawable.ic_about);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) 
    {
        // Handle item selection
        switch (item.getItemId()) {
            case 1:
                newGame();
                return true;

            default:
                return super.onOptionsItemSelected(item);
        }
    }

    private void newGame() 
    {
        System.exit(0);
        Log.d("menu", "SO FAR SO GOOD");
    }

    private View.OnClickListener mStartListener15 = new View.OnClickListener()
    {
        public void onClick(View view)
        {
//             SharedPreferences sharedPref = Colors.this.getPreferences(Context.MODE_PRIVATE);
//             SharedPreferences.Editor editor = sharedPref.edit();
//             editor.putInt(getString(R.string.max_game_score), Integer.parseInt(eText.getText().toString()));
//             editor.commit();
            Intent returnIntent = new Intent();
            returnIntent.putExtra("result", "15");
            CheckBox hardCheckBox = (CheckBox) findViewById(R.id.hardBox);
            returnIntent.putExtra("hard", hardCheckBox.isChecked());
            setResult(MainActivity.RESULT_OK, returnIntent);
            finish();
        }
    };

    private View.OnClickListener listenTwo = new View.OnClickListener() 
    {
        public void onClick(View view)
        {
            if (answer_ == 1)
                finish();
            else
                updateGame();
        }
    };

    private View.OnClickListener listenThree = new View.OnClickListener() 
    { 
        public void onClick(View view)
        {
            if (answer_ == 2)
                finish();
            else
                updateGame();
        }
    };

    private View.OnClickListener listenOne = new View.OnClickListener()
    {
        public void onClick(View view)
        {
            if (answer_ == 0)
                finish();
            else
                updateGame();

//            Intent returnIntent = new Intent();
//            returnIntent.putExtra("result", "5");
//            CheckBox hardCheckBox = (CheckBox) findViewById(R.id.hardBox);
//            returnIntent.putExtra("hard", hardCheckBox.isChecked());
//            setResult(MainActivity.RESULT_OK, returnIntent);
//            finish();
        }
    };


    private View.OnClickListener mStartListener10 = new View.OnClickListener()
    {
        public void onClick(View view)
        {
            Intent returnIntent = new Intent();
            returnIntent.putExtra("result", "10");
            CheckBox hardCheckBox = (CheckBox) findViewById(R.id.hardBox);
            returnIntent.putExtra("hard", hardCheckBox.isChecked());
            setResult(MainActivity.RESULT_OK, returnIntent);
            finish();
        }
    };

}
