using System.Diagnostics;

namespace 抖音爬虫
{
    internal class PythonAction
    {
        string searchExe;
        string findUserExe;
        Process p;
        string user_agent;
        string cookie;
        PythonAction()
        {
            searchExe = @"Search\s_complier.exe";
            findUserExe = @"FindUser\u_complier.exe";
            p = new Process();
            p.StartInfo.UseShellExecute = false; //必需
            p.StartInfo.RedirectStandardOutput = true;//输出参数设定
            p.StartInfo.RedirectStandardInput = true;//传入参数设定
            p.StartInfo.CreateNoWindow = true;
        }
        private static PythonAction pythonAction = null;
        public static PythonAction Instance
        {
            get
            {
                if (pythonAction == null)
                {
                    return pythonAction = new PythonAction();
                }
                return pythonAction;
            }
        }
        public void Init(string user_agent, string cookie)
        {
            this.user_agent = user_agent;
            this.cookie = cookie;
        }
        public string SearchImage(string keyword, string dic, string u_admid, string i_admid)
        {
            p.StartInfo.FileName = searchExe;//需要执行的文件路径
            p.StartInfo.Arguments = $"\"{keyword}\" \"{this.cookie}\" \"{this.user_agent}\" \"{dic}\" \"{u_admid}\" \"{i_admid}\"";//参数以空格分隔，如果某个参数为空，可以传入””
            p.Start();
            //阻塞
            string output = p.StandardOutput.ReadToEnd();
            p.WaitForExit();//关键，等待外部程序退出后才能往下执行}
            p.Close();
            return output;
        }
        public string FindUserImage(string urlc, string dic)
        {
            p.StartInfo.FileName = findUserExe;//需要执行的文件路径
            p.StartInfo.Arguments = $"\"{urlc}\" \"{this.cookie}\" \"{this.user_agent}\" \"{dic}\"";
            p.Start();
            //阻塞
            string output = p.StandardOutput.ReadToEnd();
            p.WaitForExit();//关键，等待外部程序退出后才能往下执行}
            p.Close();
            return output;
        }
    }
}
