// See https://aka.ms/new-console-template for more information
using Newtonsoft.Json.Linq;
using System.Text;

Console.WriteLine("Hello, World!");



var allLines = File.ReadAllLines("data.txt");

StringBuilder stringBuilder = new StringBuilder();
var listLines = new List<string>();

var dupData = new List<string>();


foreach (var str in allLines)
{
    JObject json = JObject.Parse(str);

    var data = json["data"].ToString();

    if (dupData.Contains(data))
    {
        continue;
    }
    dupData.Add(data);

    var label = json["label"];


    var listLabel = new List<string>();
    foreach (var item in label)
    {
        listLabel.Add($"[\"{item[2]}\", \"{item[3]}\"]");
    }
    var labelString = String.Join(", \r\n", listLabel);

    listLines.Add($@"{{
    ""data"": ""{data.Replace("\t"," ")}"",
    ""label"":[
        {labelString}
    ]
}}");
}
var result = String.Join(", \r\n", listLines);
using (StreamWriter writer = new StreamWriter("dataset.json"))
{
    writer.WriteLine("[");

    writer.WriteLine(result);

    writer.WriteLine("]");
}

