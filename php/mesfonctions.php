<?php
require_once("outils.php");

function factoriel($nbr){
    $p=1;
    if ($nbr!=0){
        for($i=1;$i<=$nbr;$i++){
            $p*=$i;}
        return($p);
    }
    else{
        return($p);
    }
}
function palindrome($character){
    if(strrev($character)==$character){
        return("palindrome");
    }
    else{
        return("not a palindrome");
    }}

function ecrirenbcmmot($n){
$number =array(0=>"zero",1=>"un",2=>"deux",3=>"trois",4=>"quatre",5=>"cinq",6=>"six",7=>"sept",8=>"huit",9=>"neuf");
$string=(string)$n;
$result="";
for($i=0;$i<strlen($nbr);$i++){
    $u=$string[$i];
    $result.=$number[$u]." ";
    }
return $result;
}

function triangle($nbrligne){
$p=1;
for($i=0;$i<$nbrligne;$i++){
    for($j=0;$j<=($nbrligne-$i);$j++){
        echo " ";
    }
    for($k=0;$k<=$i;$k++){
        if ($i==0 or $k==0){
            $p=1;
        }
        else{
            $p=$p*($i-$k+1)/$k;
        }
        echo $p;
    }
    echo "<br />";
}
}

function Fibonacci($n){
    $nbr1=0;
    $nbr2=1;
    $counter = 0;
    while($counter<$n){
        echo ' '.$nbr1;
        $nbr3= $nbr2+$nbr1;
        $nbr1=$nbr2;
        $nbr2=$nbr3;
        $counter = $counter + 1;
    }
}

function bissextile($annee){
    if((is_int($annee/4)&& !is_int($annee/100)) || is_int($annee/400)){
        return "TRUE";
    }
    else{
        return "FALSE";
    }

}

function table_de_multiplication($n){
    for ($i=0;$i<=10;$i++){
        $u=$i*$n;
        echo "$i * $n = $u <br />";
    }

}

function image_nombre($num){
    $chiffres= str_split($num);
    sort($chiffres);
    $nombre_ordre_croissant = implode('',$chiffres);
    rsort($chiffres);
    $nombre_ordre_decroissant = implode('',$chiffres);
    $nombre= $nombre_ordre_decroissant - $nombre_ordre_croissant;
    return $nombre;}

function damier($m,$n){
    for($row=1;$row<=$m;$row++){
        for($col=1;$col<=$n;$col++){
            $total=$row+$col;
            if($total%2 == 0){
                echo '<td style = "width: 50px; height: 30px; background: #000"></td>';

            }else{
                echo '<td style = "width: 50px; height: 30px; background: #fff"></td>';
            }
        }
    echo "</tr>";
    }
}

function unique($tableau){
    $unique=array_unique($tableau);
    return($unique);

}
//foreach(unique($tableau) as $cle => $valeur){
//    echo "\n$cle ===> $valeur <br />";}"

function repres_base2($n){
    $val_binary=decbin($n);
    $str_binary= strval($val_binary);
    
    $string=base_convert($val_binary, 2, 16);
    return $string;
}

function is_prog_arith($tableau){
    $nb_elements= count($tableau);
    if ($nb_elements<=1){
        return false;
    }
    $rapport_prog = $tableau[1] - $tableau[0];
    for($i=1;$i<$nb_elements;$i++){
        if ($tableau[$i]-$tableau[$i-1] != $rapport_prog){
            return false;
        }
    }
return true;
}

function affichage_tableau($data){
echo "<table>";
echo "<tr><th>first name</th><th>Last name</th><th>Email</th></tr>";
foreach($data as $row){
    echo "<tr>";
    foreach($row as $cell){
        echo "<td>$cell</td>";
    }
    echo "</tr>";
}
echo "</table>";
}

function is_minuscule($chaine){
    for($sc=0;$sc<strlen($chaine);$sc++){
        if (ord($chaine[$sc])>= ord('A') && ord($chaine[$sc])<= ord('Z')){
            return "yes";
        }
    }
    return "no";
}

function affichetable_recur($data){
    echo "<table>";
    foreach ($data as $key => $value) {
        echo "<tr>";
        if (is_array($value)){
            echo "<td>".$key."</td>";
            echo "<td>";
            affichetable($value);
            echo "</td>";
        }else{
            echo "<td>".$key."</td>";
            echo "<td>".$value."</td>";
        }
        echo "</tr>";
    }
    echo "</table>";
}

function date_mots(){
$joursemaine =date('w');
$jourmois = date('d');
$mois = date('n');
$annee = date('Y');

$joursSemaine = array('dimanche','lundi','mardi','mercredi','jeudi','vendredi','samedi');
$moisannee = array('janvier','fevrier','mars','avril','mai','juin','juillet','aout','septembre','octobre','novembre','decembre');

return $joursSemaine[$joursemaine].' '.$jourmois.' '.$moisannee[$mois - 1].' '.$annee;

}

function pos_letter($letter){
    $position = ord($letter)-ord('a');
    return $position;
}

?>
