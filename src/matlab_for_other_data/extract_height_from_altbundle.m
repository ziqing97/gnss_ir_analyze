function[t,h] = extract_height_from_altbundle(object)
% time
cropTime = object.ObjCropData.Raw.Sat.Lat.Hi.Ku.Time;
t = datetime(cropTime, "ConvertFrom","datenum",'TimeZone','UTC');

% alt
alt = object.ObjCropData.Raw.Sat.Alt.Hi.Ku.Signal;

% range
cropRange = eval(['object.ObjCropData.' (object.ObjTS.deepA.range)]);

% corrction
CorsName = fieldnames(object.ObjTS.deepA);
cropCors = zeros(length(cropTime),1);
for Cors = 3:numel(CorsName)
    if ~isempty(object.ObjTS.deepA.(CorsName{Cors}))
        eval(['cropCors = cropCors + object.ObjCropData.' (object.ObjTS.deepA.(CorsName{Cors})) ';']);
    end
end

% height
h = alt - cropRange - cropCors;
end