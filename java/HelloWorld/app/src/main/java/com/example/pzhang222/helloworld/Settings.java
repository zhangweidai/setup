package com.example.pzhang222.helloworld;

import android.content.Intent;
import android.os.Bundle;
import android.app.Activity;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;

public class Settings extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) 
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings2);

        Button finishBtn = (Button) findViewById(R.id.button5);
        finishBtn.setOnClickListener(mStartListener5);

        finishBtn = (Button) findViewById(R.id.button10);
        finishBtn.setOnClickListener(mStartListener10);

        finishBtn = (Button) findViewById(R.id.button15);
        finishBtn.setOnClickListener(mStartListener15);
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
//             SharedPreferences sharedPref = Settings.this.getPreferences(Context.MODE_PRIVATE);
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


    private View.OnClickListener mStartListener5 = new View.OnClickListener()
    {
        public void onClick(View view)
        {
//             SharedPreferences sharedPref = Settings.this.getPreferences(Context.MODE_PRIVATE);
//             SharedPreferences.Editor editor = sharedPref.edit();
//             editor.putInt(getString(R.string.max_game_score), Integer.parseInt(eText.getText().toString()));
//             editor.commit();
            Intent returnIntent = new Intent();
            returnIntent.putExtra("result", "5");
            CheckBox hardCheckBox = (CheckBox) findViewById(R.id.hardBox);
            returnIntent.putExtra("hard", hardCheckBox.isChecked());
            setResult(MainActivity.RESULT_OK, returnIntent);
            finish();
        }
    };


    private View.OnClickListener mStartListener10 = new View.OnClickListener()
    {
        public void onClick(View view)
        {
//             SharedPreferences sharedPref = Settings.this.getPreferences(Context.MODE_PRIVATE);
//             SharedPreferences.Editor editor = sharedPref.edit();
//             editor.putInt(getString(R.string.max_game_score), Integer.parseInt(eText.getText().toString()));
//             editor.commit();
            Intent returnIntent = new Intent();
            returnIntent.putExtra("result", "10");
            CheckBox hardCheckBox = (CheckBox) findViewById(R.id.hardBox);
            returnIntent.putExtra("hard", hardCheckBox.isChecked());
            setResult(MainActivity.RESULT_OK, returnIntent);
            finish();
        }
    };

}
