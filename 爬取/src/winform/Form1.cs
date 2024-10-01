using System;
using System.IO;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace 抖音爬虫
{
    public partial class Form1 : Form
    {
        bool findUser;
        bool Search;
        public Form1()
        {
            InitializeComponent();
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(Save);
            Init();
        }

        private void radioButton1_CheckedChanged(object sender, EventArgs e)
        {
            Search = radioButton1.Checked;
            findUser = radioButton2.Checked;
        }
        private void PrintLog(string result)
        {
            richTextBox3.AppendText(result);
        }
        private void Init()
        {
            try
            {
                string filePath = @"config.ini";
                string[] content = File.ReadAllLines(filePath, Encoding.UTF8);
                if (content.Length <= 0)
                {
                    PrintLog("暂无配置文件，需完成一次使用");
                    return;
                }
                richTextBox1.Text = content[0];
                richTextBox2.Text = content[1];
                textBox1.Text = content[2];
            }
            catch (Exception ex)
            {
                PrintLog("初始化失败" + ex.Message);
            }
        }

        private void Save(Object sender, FormClosingEventArgs e)
        {
            try
            {
                string filePath = @"config.ini";
                string cookie = richTextBox1.Text;
                string userAgent = richTextBox2.Text;
                string Down_directory = textBox1.Text;

                // 使用StreamWriter来写入多行文本
                using (StreamWriter writer = new StreamWriter(filePath, false, Encoding.UTF8))
                {
                    writer.WriteLine(cookie);
                    writer.WriteLine(userAgent);
                    writer.WriteLine(Down_directory);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("创建配置失败：" + ex.Message);
            }
        }

        private void label1_Click(object sender, EventArgs e)
        {

        }

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void label3_Click(object sender, EventArgs e)
        {

        }

        private void label3_Click_1(object sender, EventArgs e)
        {

        }

        private async void button1_Click(object sender, EventArgs e)
        {
            string keyword = richTextBox4.Text;
            string dic = textBox1.Text;
            string result = "";
            PythonAction.Instance.Init(richTextBox2.Text, richTextBox1.Text);
            if (Search)
            {
                string u_admid = textBox2.Text;
                string i_admid = textBox4.Text;
                Task<string> task = Task.Run(() =>
                {
                    return PythonAction.Instance.SearchImage(keyword, dic, u_admid, i_admid);
                });
                result = await task;
            }
            if (findUser)
            {
                string url = richTextBox5.Text;
                Task<string> task = Task.Run(() =>
                {
                    return PythonAction.Instance.FindUserImage(url, dic);
                });
                result = await task;
            }
            PrintLog(result);
        }

        private void label4_Click(object sender, EventArgs e)
        {

        }

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void label5_Click(object sender, EventArgs e)
        {

        }

        private void label5_Click_1(object sender, EventArgs e)
        {

        }

        private void textBox2_TextChanged(object sender, EventArgs e)
        {

        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void radioButton2_CheckedChanged(object sender, EventArgs e)
        {
            findUser = radioButton2.Checked;
            Search = radioButton1.Checked;
        }

        private void richTextBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void richTextBox2_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBox4_TextChanged(object sender, EventArgs e)
        {

        }

        private void label9_Click(object sender, EventArgs e)
        {

        }
    }
}
