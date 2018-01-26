% dat=function read_fromGNUradio(path,type,varargin)
% reads data from file sinks in gnuradio
%
% path: file to read
% type: 'complex', 'float'|'float32', 'int'|'int32', 'short'|'int16', 'byte'|'char'
% varargin = 
%    - Ndat: Number of data to be read from file
% 
% Germán Augusto Ramírez Arroyave
% Universidad Nacional de Colombia 
% CMUN July, 2017

function data=read_fromGNUradio(file_path,kind,varargin)
	if ~isempty(varargin)
        Ndat=varargin{1};
    else
        Ndat=inf;
	end
	fp=fopen(file_path,'rb');
    if fp
        switch(kind)
            case 'complex'     % fread is used due to its binary reading capabilities
                tmp=fread(fp,[2,Ndat],'float32'); % Shape of the original file
                data=tmp(1,:)+1i*tmp(2,:);
                data=data.';
            case {'float','float32'}
                data=fread(fp,Ndat,'float32');
            case {'int','int32'}
                data=fread(fp,Ndat,'int32');
            case {'short','int16'}
                data=fread(fp,Ndat,'int16');
            case {'byte','char'}
                data=fread(fp,Ndat,'char'); % tests must be performed to save and read this kind of data
            otherwise
                disp('Specified kind of data is not supported, load failed');
        end
        fclose(fp);
    else 
        error('Path or file corrupted, load failed');
    end
return