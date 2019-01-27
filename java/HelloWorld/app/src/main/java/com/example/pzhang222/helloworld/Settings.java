package com.example.pzhang222.helloworld;

import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.app.Activity;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;

public class Settings extends Activity {

    private Button finishBtn_;

    @Override
    protected void onCreate(Bundle savedInstanceState) 
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings2);
        finishBtn_ = (Button) findViewById(R.id.button);
        finishBtn_.setOnClickListener(mStartListener);
    }

    private View.OnClickListener mStartListener = new View.OnClickListener()
    {
        public void onClick(View view)
        {
//             SharedPreferences sharedPref = Settings.this.getPreferences(Context.MODE_PRIVATE);
//             SharedPreferences.Editor editor = sharedPref.edit();
//             editor.putInt(getString(R.string.max_game_score), Integer.parseInt(eText.getText().toString()));
//             editor.commit();
//
            Intent returnIntent = new Intent();

            EditText eText = (EditText) findViewById(R.id.MaxGameScore);
            returnIntent.putExtra("result", eText.getText().toString());

            CheckBox hardCheckBox = (CheckBox) findViewById(R.id.hardBox);
            returnIntent.putExtra("hard", hardCheckBox.isChecked());

            setResult(MainActivity.RESULT_OK, returnIntent);

            finish();
        }
    };

}
