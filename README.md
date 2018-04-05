# sdor
Swift Directory Object Remover

Something (cloudfuse?) was leaving empty directory objects all over our swift store. Some other tools (like Alluxio) were unable to handle these, leaving them to 'mask' any objects with that directory in their name.

Use with caution!
