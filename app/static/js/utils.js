var notificationPopup = function(title, message, status, icon){
    var color;
    if (status == 'success'){
        color = '#7DC27D';
    }else if (status == 'error'){
        color = '#A90329';
    }else if (status == 'warning'){
        color = '#efe1b3';
    }else{
        color = '#d6dde7';
    }
    $.smallBox({
        title : title,
        content : message,
        color : color,
        timeout: 8000,
        icon : icon
    });

};