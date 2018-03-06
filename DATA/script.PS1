$path = "C:\Users\ist181159\Desktop\2semestre\MLProject\dotsandboxes-master\DATA"
new-item $path\exp -itemtype directory
$count = [System.IO.Directory]::GetFiles($path).Count
For ($i=1; $i -le $count-1; $i++) {
    magick newesttree$i.svg exp/experiment_$i.png 
    }