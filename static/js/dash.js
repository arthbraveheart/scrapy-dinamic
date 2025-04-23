var dagcomponentfuncs = (window.dashAgGridComponentFunctions = window.dashAgGridComponentFunctions || {});

dagcomponentfuncs.SellerLink = function (props) {
    return React.createElement (
        'a' ,
        {href: props.value , target: '_blank'} ,
        'View'
    );
};