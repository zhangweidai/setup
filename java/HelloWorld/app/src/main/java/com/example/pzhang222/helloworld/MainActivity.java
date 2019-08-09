package com.example.pzhang222.helloworld;

import android.app.Activity;
import android.content.Intent;
import android.content.res.Resources;
import android.graphics.Color;
import android.graphics.drawable.ColorDrawable;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.util.DisplayMetrics;
import android.util.Log;
import android.util.TypedValue;
import android.view.Gravity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.Button;
import android.widget.GridLayout;
import android.widget.LinearLayout;
import android.widget.Space;
import android.widget.TextView;

import java.util.List;
import java.util.Random;
import java.util.Vector;

public class MainActivity extends Activity
{
    private TextView score_;
    private TextView rounds_;
    private Boolean showingAnswer_ = false;
    private int missCount_ = 0;
    private int maxScore_ = 10;
    private int columnCount_ = 4;
    private int btnWidth_ = 80;
    private int winCount_ = 0;
    private int gameCount_ = 0;
    private int recallCount_ = 5;
    private int totalTiles_ = 24;
    private int curGuessIdx_ = 0;
    private static List<Button> buttonList_ = new Vector<Button>();
    private static List<Integer> answerStack_ = new Vector<Integer>();
    private static List<Integer> retryStackBack_ = new Vector<Integer>();
    private static List<Integer> retryStack_ = new Vector<Integer>();

    @Override
    public void onCreate(Bundle savedInstanceState) 
    {
        super.onCreate(savedInstanceState);   
        getWindow().getDecorView().setBackgroundColor(Color.GRAY);

        Intent intent = new Intent(this, Settings.class);
        startActivityForResult(intent, 1);
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

    private Boolean isEasyMode()
    {
        return (columnCount_ == 4);
    }

    private void createGameBoard()
    {
        createGameBoard(false);
    }

    private GridLayout getGameButtonLayout()
    {
        GridLayout retLayout = new GridLayout(this);
        int row = totalTiles_ / columnCount_;
        retLayout.setAlignmentMode(GridLayout.ALIGN_BOUNDS);
        retLayout.setColumnCount(columnCount_);
        retLayout.setRowCount(row + 1);

        buttonList_.clear();

        Resources res = getResources();
        DisplayMetrics dm = res.getDisplayMetrics();
        int width = (int) TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, btnWidth_, res.getDisplayMetrics());

        int display = getResources().getDisplayMetrics().widthPixels;
        int converted = (int) TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, display, res.getDisplayMetrics());
        Log.d("whatnow", Integer.toString(display));
        Log.d("whatnow", Integer.toString(converted));

        display = getResources().getDisplayMetrics().heightPixels;
        converted = (int) TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, display, res.getDisplayMetrics());
        Log.d("whatnow", Integer.toString(display));
        Log.d("whatnow", Integer.toString(converted));

        int sw = dm.widthPixels;
        int sh = dm.heightPixels;

        converted = (int) TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, 20, res.getDisplayMetrics());
        int adjust = row * converted;
        int margin = (sw + sh) / adjust;

        int hx = (sh-adjust) / row;
        int wx = (sw-(columnCount_ * 10)) /columnCount_;

        Button btn;
        for (int icount = 0, col = 0, rr = 0; icount < totalTiles_; icount++, col++)
        { 
            if (col == columnCount_)
            { 
                col = 0;
                rr++;
            } 

            btn = new Button(this);
            btn.setId(icount);
            btn.setBackgroundColor(Color.LTGRAY);
            btn.setOnClickListener(tileClicked);

            btn.setText(Integer.toString(icount));
            btn.setWidth(wx);
            btn.setHeight(hx);
            retLayout.addView(btn, icount);

            GridLayout.LayoutParams param = new GridLayout.LayoutParams();
            param.height = GridLayout.LayoutParams.WRAP_CONTENT;
            param.width = GridLayout.LayoutParams.WRAP_CONTENT;
            param.rightMargin = margin;
            param.topMargin = margin;
            param.setGravity(Gravity.CENTER_VERTICAL | Gravity.CENTER_HORIZONTAL);
            param.columnSpec = GridLayout.spec(col);
            param.rowSpec = GridLayout.spec(rr);

            btn.setLayoutParams (param);
            buttonList_.add(btn);
        } 

            GridLayout.LayoutParams huh = new GridLayout.LayoutParams();
            huh.rightMargin = 20;
            huh.topMargin = 20;
            huh.bottomMargin = 20;
            huh.leftMargin = 20;

//        retLayout.setUseDefaultMargins(true);
        retLayout.setLayoutParams(huh);
        return retLayout;
    }

//    private Button getExitBtn()
//    {
//        Button btn = new Button(this);
//        btn.setText("Exit");
//        btn.setOnClickListener(mExitListener);
//        btn.setId(99);
//        return btn;
//    }

    private Button getStartBtn()
    {
        Button btn = new Button(this);
        btn.setText("Start");
        btn.setOnClickListener(mStartListener);
        btn.setId(100);
        return btn;
    }

    private void createGameBoard(Boolean starting)
    {
        LinearLayout bottomLayout = new LinearLayout(this);
        bottomLayout.setOrientation(0);
        LinearLayout mainLayout = new LinearLayout(this);
        mainLayout.setOrientation(1);

        if (starting)
            mainLayout.addView(getGameButtonLayout());

        mainLayout.addView(bottomLayout);

        if (!starting)
            bottomLayout.addView(getStartBtn());

        score_ = new TextView(this);
        score_.setText("0 points / ");

        rounds_ = new TextView(this);
        rounds_.setText(" ( Press Start ) ");

        Space space = new Space(this);
        space.setMinimumWidth(30);
        bottomLayout.addView(space);
        bottomLayout.addView(score_);
        bottomLayout.addView(rounds_);

        mainLayout.setGravity(Gravity.CENTER_VERTICAL | Gravity.CENTER_HORIZONTAL);
        setContentView(mainLayout);
    }

    public void setHard()
    {
        recallCount_ = recallCount_ + 1;
        columnCount_ = 5;
        totalTiles_ = 35;
        btnWidth_ = 65;
    }


    private View.OnClickListener mStartListener = new View.OnClickListener() 
    {
        public void onClick(View view)
        {
            Intent intent = new Intent(view.getContext(), Settings.class);
            startActivityForResult(intent, 1);
        }
    };

	@Override
	protected void onActivityResult(int requestCode, int resultCode, Intent data) 
    {
        if (requestCode == 1) 
        {
            if (resultCode == Activity.RESULT_OK)
            {
                String result = data.getStringExtra("result");
                maxScore_ = Integer.parseInt(result);

                Boolean hard = data.getBooleanExtra("hard", false);
                if (hard)
                    setHard();

                createGameBoard(true);

                startGame();

            }
        }
    }

    private View.OnClickListener mExitListener = new View.OnClickListener() 
    {
        public void onClick(View vew) 
        {
            System.exit(0);
        }
    };

    private void startFromRetry()
    {
        Log.d("retrying", "starting retry");
        answerStack_ = new Vector(retryStack_);
        int icount = 1;
        for (int var : answerStack_)
        {
            Log.d("retrying", String.format("Using %d", var));
            Button object;
            object = buttonList_.get(var);
            object.setText(Integer.toString(icount));
            if (icount == 1)
                object.setBackgroundColor(Color.GREEN);
            ++icount;
        }
    }

    private void startFromNew()
    {
        Log.d("joined", "starting new");
        for (int icount = 1; icount <= recallCount_; ++icount)
        {
            int rand = 0;
            Button object;
            do 
            {
                rand = getRandomButtonIndex();
                object = buttonList_.get(rand);
            } 
            while (!object.getText().equals(""));
            Log.d("myTag", String.format("added to answerStack_ %d", rand));
            Log.d("myTag", Integer.toString(icount));
            answerStack_.add(rand);

            object.setText(Integer.toString(icount));

            if (icount == 1)
                object.setBackgroundColor(Color.GREEN);
        }

    }

    private void startGame()
    {
        Log.d("retrying", "starting a game");
        curGuessIdx_ = 0;
        gameCount_ = gameCount_ + 1;
        answerStack_.clear();
        rounds_.setText(String.format((" Round %d"), gameCount_));
        getWindow().getDecorView().setBackgroundColor(Color.WHITE);

        // reset all to grey
        final int size = buttonList_.size();
        for (int icount = 0; icount < size; ++icount)
        {
            Button object = buttonList_.get(icount);
            object.setText("");
            object.setBackgroundColor(Color.LTGRAY);
        }

        if (retryStack_.isEmpty())
        {
            startFromNew();
        }
        else
        {
            startFromRetry();
            retryStack_.clear();
        }

        if (!retryStackBack_.isEmpty())
        {
            retryStack_ = new Vector(retryStackBack_);
            retryStackBack_.clear();
            Log.d("retrying", "clearing retry stack back");
        }
    }

    private List<Integer> modifiedAnswerStack()
    {
        int index = new Random().nextInt(answerStack_.size());
        int rand = 0;
        do 
        {
            rand = getRandomButtonIndex();
        } 
        while (answerStack_.contains(rand));

        answerStack_.set(index, rand);
        return answerStack_;
    }

    private void showAnswer()
    {
        showingAnswer_ = true;
        for (int icount = 0, col = 0, rr = 0; icount < totalTiles_; icount++, col++)
        { 
            if (col == columnCount_)
            { 
                col = 0;
                rr++;
            } 

            int cButtonId = buttonList_.get(icount).getId();
            Log.d("myTag", Integer.toString(cButtonId));
            int answer = answerStack_.indexOf(cButtonId);
            if (answer != -1)
            {
                buttonList_.get(icount).setText(Integer.toString(answer + 1));
            }
        }

        retryStackBack_ = new Vector(modifiedAnswerStack());
        missCount_++;
        if (missCount_ > 4 && winCount_ > 1)
        {
            winCount_--;
            missCount_ = 0;
            score_.setText(String.format(("%d points / "), winCount_));
        }
    }


    private View.OnClickListener tileClicked = new View.OnClickListener() 
    {
        public void onClick(View vew) 
        {
            if (!(vew instanceof Button))
                return;

            Button btn = (Button) vew;
            if (showingAnswer_)
            {
                showingAnswer_ = false;
                startGame();
                return;
            }

            int cId = btn.getId();
            Log.d("myTag", Integer.toString(cId));
            Log.d("curGuessIdx_", Integer.toString(curGuessIdx_));

            if (answerStack_.get(curGuessIdx_) == cId)
            {
                // correct
                btn.setText(Integer.toString(curGuessIdx_ + 1));
                getWindow().getDecorView().setBackgroundColor(Color.WHITE);
                curGuessIdx_++;
                if (curGuessIdx_ == 1)
                    hideAll();
                btn.setText(Integer.toString(curGuessIdx_));
                btn.setBackgroundColor(Color.WHITE);
            }
            else
            {
                // incorrect
                if (curGuessIdx_ == 0)
                {
                    // message click the green button to start
                    return;
                }
                
                // already pressed?
                if (!btn.getText().equals(""))
                    return;

                if (isEasyMode())
                {
                    // ignore tiles that aren't highlighted
                    Drawable buttonBackground = btn.getBackground();
                    ColorDrawable buttonColor = (ColorDrawable) btn.getBackground();
                    int colorId = buttonColor.getColor();
                    if (colorId != Color.YELLOW)
                        return;
                }

                showAnswer();
                getWindow().getDecorView().setBackgroundColor(Color.RED);
            }

            if (curGuessIdx_ == recallCount_)
            {
                winCount_ = winCount_ + 1;
                score_.setText(String.format(("%d points / "), winCount_));
                if (winCount_ >= maxScore_)
                {
                    createGameBoard();

                    score_.setText(String.format(("%d points / "), winCount_));
                    rounds_.setText(String.format((" Round %d"), gameCount_));

                    getWindow().getDecorView().setBackgroundColor(Color.GREEN);
                    gameCount_ = 0;
                }
                else
                    startGame();
            }
        }
    };

    private void hideAll()
    {
        final int size = buttonList_.size();
        for (int icount = 0; icount < size; ++icount)
        {
            Button object = buttonList_.get(icount);
            if (!object.getText().equals("") && isEasyMode())
            {
                object.setBackgroundColor(Color.YELLOW);
            }
            object.setText("");
        }

        
        if (isEasyMode() && (maxScore_ - winCount_ <= 2))
        {
            int rand = getRandomButtonIndex();
            Button object = buttonList_.get(rand);
            object.setBackgroundColor(Color.YELLOW);
        }
    }

    private int getRandomButtonIndex()
    {
        final int min = 1;
        final int max = buttonList_.size();
        return new Random().nextInt((max - min)) + min;
    }


}
