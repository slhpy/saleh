
<?php
error_reporting(0);

define('API_KEY','22423548:gIMlXtGvzsSuzPc83zYUCTwvxLukTtQTmQ6scsVg');
function pebkabot($method,$datas=[]){$url = "https://tapi.bale.ai/bot".API_KEY."/".$method;
$ch = curl_init(); curl_setopt($ch,CURLOPT_URL,$url); curl_setopt($ch,CURLOPT_RETURNTRANSFER,true); curl_setopt($ch,CURLOPT_POSTFIELDS,$datas); $res = curl_exec($ch); return json_decode($res);}
$update = json_decode(file_get_contents('php://input'));
$message = $update->message;
$textmassage = $message->text;
if($textmassage=="/start"){
pebkabot('sendmessage',[
'chat_id'=>$message->chat->id,
'text'=>"سلام",
]);
}

?>

