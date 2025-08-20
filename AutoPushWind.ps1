while ($true) {
    $status = git status --porcelain
    if ($status) {
        Write-Output "Changes detected in repository. Committing and pushing changes..."
        git pull origin main --rebase
        git add -A
        git commit -m "Robin h00d"
        git push origin main
        Write-Output "Changes committed and pushed successfully."
    }
    Start-Sleep -Seconds 5
}


