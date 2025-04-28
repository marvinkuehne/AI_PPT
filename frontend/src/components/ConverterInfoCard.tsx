import InfoOutlineIcon from '@mui/icons-material/InfoOutline';

interface Props {
    className?: string
}

function ConverterInfoCard({ className }: Props) {
    return (
        <div className={"bg-gray-400/10 rounded p-2 flex flex-col " + className}>
            <div className="flex items-center justify-start gap-1 mb-2">
                <InfoOutlineIcon />
                <p className="font-bold">Tips for better results</p>
            </div>
            <ul className="list-disc pl-5 flex flex-col gap-1">
                <li>Make sure your diagram is constructed from straight lines</li>
                <li>Make sure your background is plain, white and clear</li>
                <li>Make sure your lines are consistent and are all the same weight</li>
            </ul>
        </div>
    );
}

export default ConverterInfoCard;