// See https://aka.ms/new-console-template for more information
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using System.Text;

Console.WriteLine("Hello, World!");

/*

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
*/


var  allText = File.ReadAllText("dataset.json");

var objects = JsonConvert.DeserializeObject<List<JObject>>(allText);

var index = 0;

var listJson = new List<string>();
foreach (var json in objects)
{
    var data = json["data"].ToString();
    var labels = json["label"];

    var subStr = data;
    var currentIndex = 0;
    var listLabel = new List<string>();
    foreach (var item in labels)
    {
        subStr = data.Substring(currentIndex, data.Length - currentIndex);
        var labelName = item[0].ToString();
        var labelValue = item[1].ToString();

        try
        {
            var startIndex = subStr.IndexOf(labelValue) + currentIndex;
            if (startIndex == 0 && currentIndex > 0)
            {
                throw new NullReferenceException(labelValue);
            }

            var endIndex = startIndex + labelValue.Length;
            currentIndex = endIndex;
            listLabel.Add($@"[{startIndex}, {endIndex}, ""{labelName}"", ""{labelValue}""]");
        }
        catch (Exception ex)
        {
            Console.WriteLine(ex);
            throw;
        }
    }
    var labelString = $@"[{string.Join(',', listLabel)}]";
    listJson.Add($@"{{""id"": {index}, ""data"": ""{data}"", ""label"": {labelString}}}");
    index += 1;
}

var result = String.Join("\r\n", listJson);
using (StreamWriter writer = new StreamWriter("labeled_dataset.jsonl"))
{
    writer.WriteLine(result);
}
