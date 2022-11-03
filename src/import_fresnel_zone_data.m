function Untitled = import_fresnel_zone_data(filename, dataLines)
%IMPORTFILE 从文本文件中导入数据
%  UNTITLED = IMPORTFILE(FILENAME)读取文本文件 FILENAME 中默认选定范围的数据。  以表形式返回数据。
%
%  UNTITLED = IMPORTFILE(FILE, DATALINES)按指定行间隔读取文本文件 FILENAME
%  中的数据。对于不连续的行间隔，请将 DATALINES 指定为正整数标量或 N×2 正整数标量数组。
%
%  示例:
%  Untitled = importfile("C:\Users\yuziq\Documents\gnss_ir_analyze\src\20220811-2.csv", [2, Inf]);
%
%  另请参阅 READTABLE。
%
% 由 MATLAB 于 2022-11-03 12:00:35 自动生成

%% 输入处理

% 如果不指定 dataLines，请定义默认范围
if nargin < 2
    dataLines = [2, Inf];
end

%% 设置导入选项并导入数据
opts = delimitedTextImportOptions("NumVariables", 8);

% 指定范围和分隔符
opts.DataLines = dataLines;
opts.Delimiter = ",";

% 指定列名称和类型
opts.VariableNames = ["VarName1", "satellite", "north", "east", "height", "lat_center", "lon_center", "height_center"];
opts.VariableTypes = ["double", "string", "double", "double", "double", "double", "double", "double"];

% 指定文件级属性
opts.ExtraColumnsRule = "ignore";
opts.EmptyLineRule = "read";

% 指定变量属性
opts = setvaropts(opts, "satellite", "WhitespaceRule", "preserve");
opts = setvaropts(opts, "satellite", "EmptyFieldRule", "auto");

% 导入数据
Untitled = readtable(filename, opts);

end