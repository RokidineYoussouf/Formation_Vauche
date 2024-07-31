<!DOCTYPE html>
<html>
<head>
    <title>Stockage d'images</title>
</head>
<body>

<h1>Stockage d'images</h1>

<form method="post" enctype="multipart/form-data" action="">
    <label for="nom">Nom de l'image:</label>
    <input type="text" id="nom" name="nom" required>
    <label for="description">Description:</label>
    <textarea id="description" name="description"></textarea>
    <label for="image">Image:</label>
    <input type="file" id="image" name="image" accept="image/*" required>
    <input type="submit" value="Envoyer">
</form>

<?php

// Vérifier si le formulaire a été posté
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Vérifier si le nom de l'image existe déjà
    $nom = $_POST["nom"];
    $pdo = new PDO("mysql:host=localhost;dbname=examen2024", "examen2024", "examen2024");
    $requete = $pdo->prepare("SELECT * FROM liens WHERE Nom = :nom");
    $requete->bindParam(":nom", $nom);
    $requete->execute();
    $resultat = $requete->fetch(PDO::FETCH_ASSOC);
    if ($resultat) {
        echo "Une image avec ce nom existe déjà. Veuillez choisir un autre nom.";
    } else {
        // Enregistrer les données de l'image
        $description = $_POST["description"];
        $image_tmp = $_FILES["image"]["tmp_name"];
        $image_name = basename($_FILES["image"]["name"]);
        $image_path = "images/" . $image_name;
        if (move_uploaded_file($image_tmp, $image_path)) {
            $lien = "/images/" . $image_name;
            $requete = $pdo->prepare("INSERT INTO liens (Nom, Description, Lien) VALUES (:nom, :description, :lien)");
            $requete->bindParam(":nom", $nom);
            $requete->bindParam(":description", $description);
            $requete->bindParam(":lien", $lien);
            $requete->execute();
            echo "Image enregistrée avec succès.";
        } else {
            echo "Erreur lors de l'enregistrement de l'image.";
        }
    }
}

// Afficher les images
$pdo = new PDO("mysql:host=localhost;dbname=examen2024", "examen2024", "examen2024");
$requete = $pdo->query("SELECT * FROM liens");
echo "<table>";
echo "<tr><th>Nom</th><th>Image</th></tr>";
while ($image = $requete->fetch(PDO::FETCH_ASSOC)) {
    echo "<tr>";
    echo "<td>" . $image["Nom"] . "</td>";
    echo "<td><img src=\"" . $image["Lien"] . "\" width=\"100\" height=\"100\"></td>";
    echo "</tr>";
}
echo "</table>";

?>

</body>
</html>