using System;
using System.Collections.Generic;
public class DefaultDictionary<TKey, TValue> : Dictionary<TKey, TValue> where TValue : new()
{
    public new TValue this[TKey key]
    {
        get
        {
            TValue val;
            if (!TryGetValue(key, out val))
            {
                val = new TValue();
                Add(key, val);
            }
            return val;
        }
        set { base[key] = value; }
    }
}

class HelloWorldWin 
{
    public static void Main() 
    {
        Console.WriteLine("I came from the CSC compiler :D");
        string path = "/home/zoe/setup/python/zen/openorders";
        string text = System.IO.File.ReadAllText(path);

        // Display the file contents to the console. Variable text is a string.
        System.Console.WriteLine("Contents of WriteText.txt = {0}", text);
        // Example #2
        // Read each line of the file into a string array. Each element
        // of the array is one line of the file.
        string[] lines = System.IO.File.ReadAllLines(path);

        // Display the file contents by using a foreach loop.
        System.Console.WriteLine("Contents of WriteLines2.txt = ");
        System.Console.WriteLine(lines.Length);
        SortedSet<Tuple<int, string> > sortedset_name = new SortedSet<Tuple<int, string> >();

        foreach (string line in lines)
        {
            // Use a tab to indent each line of the file.
            if (line.Contains("Buy"))
            {
                var words = line.Split('\t');
                foreach (var word in words)
                {
                    if (!word.Contains("Buy"))
                        continue;
                    var items = word.Split(' ');
                    var count = Int32.Parse(items[1]);
                    var astock = items[4];
                    Console.WriteLine("{0} {1}", count, astock);
                    sortedset_name.Add(Tuple.Create(count, astock));
                }
            }
        }

        SortedSet<int> sorted = new SortedSet<int>();
        sorted.Add(1);
        sorted.Add(2);
        System.Console.WriteLine(sorted);

        foreach (var word in sortedset_name.Reverse())
        {
            Console.WriteLine(word);
        }

        var dict = new DefaultDictionary<string, int>();
        Console.WriteLine(dict["foo"]);  // prints "0"
        dict["bar"] = 5;
        Console.WriteLine(dict["bar"]);  // prints "5"


        // Keep the console window open in debug mode.
//        Console.WriteLine("Press any key to exit.");
//        var i = System.Console.ReadKey();
//        Console.WriteLine("\t" + i.Key.ToString());
    }
}
HelloWorldWin.Main();
