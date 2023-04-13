#USAGE combine_docked_pose_and_protein.sh protein.pdb pose.pdb save_complex.pdb
cat $1 $2 | grep -eCONECT -eATOM -eHETATM -eCRYST1 | grep -v -eREMARK > $3

